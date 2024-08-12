import mysql.connector
from mysql.connector import Error
from django.utils import timezone
from dateutil.relativedelta import relativedelta


groq_api="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"
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq


class Hospitals:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='cts.mysql.database.azure.com',
                database='hospitals',
                user='atheeq',
                password='@Super123'
            )
            self.cursor = self.connection.cursor()
            print("connected successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
            self.cursor = None

    def network_hospitals(self, table_name, pincode):
        if not self.connection or not self.cursor:
            print("No connection to the database.")
            return []

        try:
            query = f"SELECT hospital_name, city, address FROM {table_name} WHERE pin = %s;"
            self.cursor.execute(query, (pincode,))
            rows = self.cursor.fetchall()
            print("returning from database")
            return rows
        except Error as e:
            print(f"Error executing query: {e}")
            return []
        

def get_balance_date(start,dur):
    policy_date= start + relativedelta(years=dur)
    now = timezone.now().date()
    difference = relativedelta(policy_date, now)
    difference_in_years = difference.years
    difference_in_months = difference.months + difference_in_years * 12
    if difference_in_years == 0:
        if difference_in_months==1:
            return f"{difference_in_months} month only"
        return f"{difference_in_months} months only"
    else:
        if difference_in_years==1:
            return f"{difference_in_years} year to go"
        return f"{difference_in_years} years to go"
    

def get_renew_details(policy_name,user_details):
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    CHROMA_PATH='chroma\policies'
    query_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings,collection_name=policy_name)
    user_query= "Renewal bonuses "
    results = query_db.similarity_search_with_score(user_query, k=2)
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    client = Groq(
        api_key=groq_api,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful health insurance patient helpdesk bot.You are approprite renewal bonuses content from policy document.User will provide their profile summary based on the summary and the content, Explain the renewal bonuses for the user with html tags.",
            },
            {
                "role":"system",
                "content":" Important to note! : Must format the output in HTML with appropriate tags like <h4>, <p>, <ul>, and <li>. Only explain the bonuses. Dont add unwanted texts like 'based on the details' , 'i will explain'"
            },
            {
                "role":"system",
                "content":context
            },
            {
                "role": "user",
                "content": user_details,
            },
        ],
        model="llama-3.1-70b-versatile",
    )
    output=chat_completion.choices[0].message.content
    return output



def get_claim_summary(request,claim_history):
    user=request.user
    profile=user.profile
    claimable_amt = profile.total_amount
    claims_summary=""
    claim_count=0
    for claims in claim_history:
        claim_count+=1
        claimable_amt-=claims.amount_claimed
        claims_summary+=f" Claim ID ->{claims.claim_id} , Claim-date->{claims.claim_date}, Claim-amt ->{claims.amount_claimed} , Treatment Info -> {claims.treatment_info} \n"
    
    claims_summary=f"Number of claims made by the user is {claim_count} \n"+claims_summary
    return (claims_summary,claimable_amt)




