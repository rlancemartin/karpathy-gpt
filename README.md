# Karpathy-GPT

## Context

This is an educational app showing how we can easily go from YouTube urls to a working, deployed Q+A assistant.

< TODO: Add diagram of the overall app flow. > 

## Step 1: URLs to VectorDB

See the notebook in `/index`

* Uses LangChain's `OpenAIWhisperParser` to convert urls to text
* Split them and add to VectorDB (Pinecone) with metadata

< TODO: Add diagram on data loading and where URLs fit into the bigger picture. >

## Step 2: Back-end

See the `karpathy_app.py` file in `/api`.

* Uses LangChain's `load_qa_chain` 
* Allows the user to easily specify the prompt in `default_prompt_template`
* Streams text back to front-end
* We deploy this FastAPI to Railway
* See README.md in `/api` for local testing

## Step 3: Front-end 

See `/nextjs` directory.

* Test locally:
```
uvicorn karpathy_app:app
npm run dev
```
