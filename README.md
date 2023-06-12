# Karpathy-GPT

## Context
 
This app is a template for using LangChain to build a LLM Q+A assistant from any set of YouTube videos.

We use Karpathy's [course on LLMs](https://www.youtube.com/@AndrejKarpathy/videos) as an example.

![image](https://github.com/rlancemartin/karpathy-gpt/assets/122662504/62eef1ab-4314-4398-8ba8-c985b5124b50)

We use LangChain to: 

(1) convert YouTube urls to text

(2) feed the text into LangChain [auto-evaluator](https://autoevaluator.langchain.com/) to test different chain parameters

(3) with our chosen parameters, build a vectorstore retriever back-end with FastAPI (deployed to Railway)

(4) stream the generated results (answer and retrieved docs) to a front-end (deployed to Vercel)

--- 

## Step 1: URLs to text

See [the notebook](https://github.com/rlancemartin/karpathy-gpt/blob/main/index/youtube_urls_to_vectordb.ipynb) in `/index` folder:

* Uses LangChain's `OpenAIWhisperParser` to convert urls to text in < 10 lines of code

## Step 2: Testing

See [the text files](https://github.com/rlancemartin/karpathy-gpt/tree/main/eval) in `/eval` folder:

* Feed the text from step 1 and, optionally, an eval set to the [auto-evaluator app](https://autoevaluator.langchain.com/playground)
* We can use this to test different parameters (see full README in the repo [here](https://github.com/langchain-ai/auto-evaluator))
* Use the UI to run experiments
* Select your best retriever, chain settings (e.g., k, split size, split overlap, etc), LLM, embeddings

![image](https://github.com/rlancemartin/karpathy-gpt/assets/122662504/0dbc676f-077b-4cea-bf3e-49a298f9c28a)

## Step 3: text to VectorDB

See [the notebook](https://github.com/rlancemartin/karpathy-gpt/blob/main/index/youtube_urls_to_vectordb.ipynb) in `/index` folder:

* Split the text from step 1 using parameters you found in step 2
* Upsert the vectors to a VectorDB (e.g., in this example, `Pinecone`) with metadata
* See this [PR / notebook](https://github.com/rlancemartin/langchain/blob/e1fa1a41d0b2d7f476627a6798e98f02ebe4a83d/docs/modules/indexes/document_loaders/examples/youtube_audio.ipynb) if you want to use locally with a different VectorDB

## Step 4: Back-end

See the `karpathy_app.py` file in `/api` folder:

* We use LangChain's `load_qa_chain` with a user specified LLM and prompt (see `default_prompt_template`)
* Given a question, this will stream answer the text back to front-end and pass the retrieved documents back
* We deploy this FastAPI API to Railway
* See README.md in `/api` for local testing instructions

## Step 5: Front-end 

See `/nextjs` directory for nextJS app:

* This will call the back-end with the query and fetch the documents / answer 
* Test the app locally by launching the back-end:
```
uvicorn karpathy_app:app
```
* To run front-end locally with you locally running back-end, simply change the source in `fetchEventSource` [here](https://github.com/rlancemartin/karpathy-gpt/blob/a338ceb8666c02b0ec7e7f47ca0a196d774d1e4d/nextjs/pages/index.tsx#L37) and [here](https://github.com/rlancemartin/karpathy-gpt/blob/a338ceb8666c02b0ec7e7f47ca0a196d774d1e4d/nextjs/pages/index.tsx#L55) to `http://localhost:8000/karpathy-docs` and `http://localhost:8000/karpathy-stream`
* To run the front-end locally, run:
```
npm run dev
```