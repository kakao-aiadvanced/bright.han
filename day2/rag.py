import os

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.prompts import PromptTemplate

loader = TextLoader("state_of_the_union.txt")

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(texts, embeddings)

retriever = vectorstore.as_retriever()
docs = retriever.invoke("what did the president say about ketanji brown jackson?")

# print(docs[0].page_content)
from langchain_core.pydantic_v1 import BaseModel, Field


class Result(BaseModel):
    response: str = Field(description="answer to query")
    relevance: str = Field(description="relevance from context and query. say yes or no")
    hallucination: str = Field(description="answer is correct and faithful to the prompt. say yes or no")


parser = JsonOutputParser(pydantic_object=Result)
prompt = PromptTemplate(
    template= "Answer the user query.\n{format_instructions}\n{query}\n ",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


query = "What is apple??"
# rag_chain = (
#         {"context": retriever | format_docs, "query": RunnablePassthrough()}
#         | prompt
#         | llm
#         | parser
# )
# result = rag_chain.invoke(query)

chain = prompt | llm | parser
result = chain.invoke({"context": docs, "query": query})

if result['relevance'] == "no":
    print("The answer is not relevant to the prompt.")
    exit(1)

if result['hallucination'] == "yes":
    print("The answer is not faithful to the prompt.")
    result = chain.invoke({"context": docs, "query": query})
    if result['hallucination'] == "no":
        exit(1)
else:
    print(result['response'])
