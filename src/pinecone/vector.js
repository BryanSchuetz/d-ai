import 'dotenv/config';
import { OpenAI } from "langchain/llms/openai";
import { PineconeClient } from "@pinecone-database/pinecone";
import { GithubRepoLoader } from "langchain/document_loaders/web/github";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { PineconeStore } from "langchain/vectorstores/pinecone";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";

const client = new PineconeClient();
await client.init({
  apiKey: '5f15935a-8d62-4346-b9c0-4aa89911c9ff',
  environment: 'asia-southeast1-gcp-free',
});
const pineconeIndex = client.Index('daisources');

const loader = new GithubRepoLoader(
  "https://github.com/BryanSchuetz/d-ai-sources",
  { branch: "master", recursive: true, unknown: "warn" }
);
const repoSources = await loader.load();
const textSplitter = new RecursiveCharacterTextSplitter({ chunkSize: 1000 });
const docs = await textSplitter.splitDocuments(repoSources);


await PineconeStore.fromDocuments(docs, new OpenAIEmbeddings(), {
  pineconeIndex,
});