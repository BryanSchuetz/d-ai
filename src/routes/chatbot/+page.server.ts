import { PineconeClient } from "@pinecone-database/pinecone";
import { PINECONE_API_KEY } from '$env/static/private';
import { PINECONE_ENVIRONMENT } from '$env/static/private';
import { RetrievalQAChain } from "langchain/chains";
import { OpenAI } from "langchain/llms/openai";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { PineconeStore } from "langchain/vectorstores/pinecone";
import { OPENAI_API_KEY } from '$env/static/private';
import type { Actions } from './$types';
import { PromptTemplate } from "langchain/prompts";

//Init a pincecone client and the vector store as a source for an OPENAI chain

  const client = new PineconeClient();
  await client.init({
    apiKey: PINECONE_API_KEY,
    environment: PINECONE_ENVIRONMENT,
  });
  const pineconeIndex = client.Index('daisources');
  const vectorStore = await PineconeStore.fromExistingIndex(
    new OpenAIEmbeddings({openAIApiKey: OPENAI_API_KEY}),
    { pineconeIndex }
  );

export const actions: Actions = {
  submit: async ({ request } : any) => {
      const promptFormData = await request.formData();
      const textPrompt = promptFormData.get('text-submission') as string;

      //Call and configure our chain 
      const model = new OpenAI({
        modelName: "gpt-4",
        temperature: 0.9,
        openAIApiKey: OPENAI_API_KEY
      });
      const template = `Given the provided context, respond to requests with generated text and sources. ALWAYS return a SOURCES part in your answer along with the generated text. If you don't know the answer to the question, just say 'I don't know about that'. DO NOT invent answers or sources.\n`;
      const prompt = new PromptTemplate({template: template, inputVariables: []});
      const chain = RetrievalQAChain.fromLLM(model, vectorStore.asRetriever(6), {returnSourceDocuments: true});
      //Wait for the form to be submitted and send the prompot to the chain
      const textResponse = await chain.call({
          query: `${textPrompt}\n\n###\n\n`,
      });
      //return the response from the chain
      return {
          response: textResponse.text,
          docs: structuredClone(textResponse.sourceDocuments),
      }
  }
}