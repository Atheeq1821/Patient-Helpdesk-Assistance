
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
def denial_assist(policy_name,user_denial,profile_summary):

    client = Groq(
        api_key=groq_api,
    )
    denial_content=denial_details()
    policy_content= policy_details(policy_name=policy_name)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.I will feed you with all the details regarding denial and the policy along with user profile summary. User will provide the claim denial reason briefly. You are supposed to match the user's denial reason and the provided content, and you have to eloborately explain the main possible reasons for claim denial based on the user profile after that explain the claim denial reason completely along with the resolution steps.",
            },
            {
                "role":"system",
                "content":"User profile summary: \n"+profile_summary
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
    print(output)
    formatted_output  = format_output(output)
    return formatted_output

