import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, openai_api_key=API_KEY)

embeddings = OpenAIEmbeddings(api_key=API_KEY)
