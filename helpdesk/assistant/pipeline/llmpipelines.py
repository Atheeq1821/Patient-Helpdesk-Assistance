groq_api="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"
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq



#embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

CHROMA_PATH='chroma\policies'
# CHROMA_PATH='chroma\policies'

def query_assist(user_query,policy_name,conversation_history):
    query_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,collection_name=policy_name)
    results = query_db.similarity_search_with_score(user_query, k=4)  #retriving relevant dpcuments from database
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    print("-------------------------------------------------------")
    client = Groq(
        api_key=groq_api,
    )
    history = ""
    try:
        for entry in conversation_history:
            history += f"User: {entry['user']}\nBot: {entry['model']}\n\n"
    except Exception as e:
        print("First convo")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful health insurance patient helpdesk bot. Provide an answer only to the asked query of the user based on the provided content of the insurance policy. Don't add hallucinations and content like based on previous conversation or based on the document and keep it straightforward.",
            },
            {
                "role":"system",
                "content":context
            },
            {
                "role": "user",
                "content": history + f"\nUser: {user_query}",
            },
        ],
        model="llama-3.1-70b-versatile",
    )
    output=chat_completion.choices[0].message.content
    return output

