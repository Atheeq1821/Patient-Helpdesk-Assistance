import streamlit as st
# import os
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import torch
#embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"

embeddings = HuggingFaceEmbeddings(model_name=model_name)

#loading local model
model = Ollama(model="llama2")

CHROMA_PATH='chroma'

def generate_pre_output(user_query,policy_name):
    print("inside llm")
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context without hallucinations:

    {context}

    ---

    Provide only the answer to the query without adding irrelevant sentences: {question}
    """

    query_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,collection_name=policy_name)

    #customized query
    query=f"{user_query} under {policy_name}"

    results = query_db.similarity_search_with_score(query, k=2)  #retriving relevant dpcuments from database
    print(results)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context_text, question=query)  #prompt for llm
    print("to the model...")
    response_text = model.invoke(prompt) #response from llm
    print("almost done...")
    return response_text


