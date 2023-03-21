from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
import requests

def get_dai_data(page):
  url = f"{page}"
  data = requests.get(url).json()
  return Document(
      page_content=(data["content"]),
      metadata={"source": f"{page}"}
  )

sources = [
    get_dai_data("https://dai-global-developments.com/post-api/mindthegap-a-development-finance-primer.json"),
    get_dai_data("https://dai-global-developments.com/post-api/one-year-on-how-one-usaid-governance-project-in-ukraine-pivoted-in-war-time.json"),
    get_dai_data("https://dai-global-developments.com/post-api/synthesizing-the-sensitive-lessons-from-a-political-economy-analysis-in-a-closed-environment.json"),
    get_dai_data("https://dai-global-developments.com/post-api/q-and-a-how-climate-finance-is-critical-to-prevent-future-backsliding.json")
]

chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="map_reduce")

def print_answer(question):
  print(
    chain(
      {
        "input_documents": sources,
        "question": question,
      },
      return_only_outputs=True,
    )["output_text"]
  )

