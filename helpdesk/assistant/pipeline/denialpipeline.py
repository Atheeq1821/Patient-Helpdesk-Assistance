
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq
from helpdesk.llm_utils import *
import os
from dotenv import load_dotenv
load_dotenv()
groq_api = os.getenv('GROQ_API_KEY')

model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
def denial_assist(user_details,policy_name,user_denial):

    client = Groq(
        api_key=groq_api,
    )
    denial_content=denial_details()
    policy_content= policy_details(policy_name=policy_name)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "When a user provides a brief reason for their claim denial, match it with the provided information, elaborate on the main possible reasons based on the user's profile, and fully explain the specific claim denial reason along with resolution steps using appropriate HTML tags."
            },
            {
                "role": "system",
                "content": " Important to note! : Must format the output in HTML with appropriate tags like <h4>, <p>, <ul>, and <li>.",
            },
            {
                "role":"system",
                "content":"User profile summary: \n"+user_details
            },
            # {
            #     "role":"system",
            #     "content":"General details about handling denials: \n"+denial_content
            # },
            {
                "role":"system",
                "content":"All the content about the user policy: \n"+policy_content
            },
            {
                "role":"user",
                "content":"User denial reason "+user_denial   
            },
            {
                "role":"user",
                "contact":"The customer service number"
            }
        ],
        model="llama-3.1-70b-versatile",
    )
    output=chat_completion.choices[0].message.content
    return output

