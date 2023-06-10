import os
import pinecone
import logging
import asyncio
from fastapi import FastAPI, Form
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import AsyncIteratorCallbackHandler

# Prompt template for QA
default_prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""

def make_llm(model_version):
    """
    Make LLM
    @param model_version: model_version
    @return: llm, callback handler
    """

    if (model_version == "gpt-3.5-turbo") or (model_version == "gpt-4"):
        callback = AsyncIteratorCallbackHandler()
        chosen_model = ChatOpenAI(model_name=model_version,streaming=True,callbacks=[callback],temperature=0)
    return chosen_model, callback

def make_chain(llm):
    """
    Make QA chain using specified default_prompt_template
    @param llm: llm for answering
    @return: qa_chain
    """ 
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=default_prompt_template)
    qa_chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)
    return qa_chain

def make_retriever(logger):
    """
    Make document retriever
    @return: Pinecone
    """
    logger.info("`Retriving docs ...`")
    
    # Set embeddings (must match your Pinecone DB)
    embedding = OpenAIEmbeddings()
    pc_api_key = os.environ.get('PINECONE_API_KEY')
    pc_region = "us-east1-gcp" 
    pc_index = "karpathy-gpt"

    # Set Pinecone 
    pinecone.init(api_key=str(pc_api_key), environment=str(pc_region))
    p = Pinecone.from_existing_index(index_name=str(pc_index), embedding=embedding)
    return p

import json
async def generate_docs(question):
    """
    @param question: question
    @return: docs
    """

    # Set up logging
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    # Model for answering 
    model = "gpt-3.5-turbo"
    llm, callback=make_llm(model)

    # Chain
    chain=make_chain(llm)

    # Retriever 
    retriever=make_retriever(logger)

    # Stream
    logger.info("`Getting docs ...`")
    docs = retriever.similarity_search(query=question,k=3) 
    for doc in docs:
        yield json.dumps({"data":{"pageContent": doc.page_content, "metadata": doc.metadata}})

async def generate_response(question):
    """
    @param question: question
    @return: answer stream
    """

    # Set up logging
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    # Model for answering 
    model = "gpt-3.5-turbo"
    llm, callback=make_llm(model)

    # Chain
    chain=make_chain(llm)

    # Retriever 
    retriever=make_retriever(logger)

    # Stream
    logger.info("`Generating answer ...`")
    docs = retriever.similarity_search(query=question,k=3) 
    task = asyncio.create_task(
        chain.acall({
            "input_documents": docs,
            "question": question
        }),
    )
    async for token in callback.aiter():
        yield token
    await task

# App 
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Karpathy GPT!"}

# Docs
@app.post("/karpathy-docs")
async def create_docs_response(
    query: str = Form("What is the difference between an encoder and decoder?"),
):
    return EventSourceResponse(generate_docs(query), headers={"Content-Type": "text/event-stream", "Connection": "keep-alive", "Cache-Control": "no-cache"})

# Answer stream
@app.post("/karpathy-stream")
async def create_response(
    query: str = Form("What is the difference between an encoder and decoder?"),
):
    # Return SSE
    return EventSourceResponse(generate_response(query), headers={"Content-Type": "text/event-stream", "Connection": "keep-alive", "Cache-Control": "no-cache"})
    