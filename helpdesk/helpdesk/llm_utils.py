groq_api="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"
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq

model_name = "sentence-transformers/all-mpnet-base-v2"

embeddings = HuggingFaceEmbeddings(model_name=model_name)

CHROMA_PATH='chroma\policies'


def policy_details(policy_name):
    query_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,collection_name=policy_name)
    documents = query_db.get(include=['documents'])
    document_content=""
    for doc in documents['documents']:
        document_content+=doc+"\n"
    return document_content

def denial_details():
    path="chroma\denial"
    query_db = Chroma(persist_directory=path, embedding_function=embeddings,collection_name='denial')
    documents = query_db.get(include=['documents'])
    document_content=""
    for doc in documents['documents']:
        document_content+=doc+"\n"
    return document_content

def get_user_summary(name,age,policy,type,gender,claims,policy_start_date,premium,amt,expiry):
    client = Groq(
        api_key=groq_api,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "provide a comprehensive summary for insurance user profile with given user information",
            },
            {
                "role":"system",
                "content":f"""
                            Name: {name}
                            Age: {age}
                            Gender: {gender}
                            Policy Name: {policy}
                            Policy Type: {type}
                            Policy Enrolled Date: {policy_start_date}
                            Policy Expiry: {expiry}
                            Premium: {premium}
                            Total Insurance Amount: {amt}
                            
                            History of claims made by the user:
                            {claims}
                            """
            },
            
        ],
        model="llama-3.1-70b-versatile",
    )
    output=chat_completion.choices[0].message.content

    return output


def denial_details():
    path="chroma\denial"
    query_db = Chroma(persist_directory=path, embedding_function=embeddings,collection_name='denial')
    documents = query_db.get(include=['documents'])
    document_content=""
    for doc in documents['documents']:
        document_content+=doc+"\n"
    return document_content

def policy_details(policy_name):
    query_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,collection_name=policy_name)
    documents = query_db.get(include=['documents'])
    document_content=""
    for doc in documents['documents']:
        document_content+=doc+"\n"
    return document_content
    
