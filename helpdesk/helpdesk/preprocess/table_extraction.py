import tabula
import pandas as pd
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


pdf_path = "./data/policy_data/hdfc/energy.pdf"  
tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

for i, table in enumerate(tables):
    excel_file = f"table_{i + 1}.xlsx"
    table.to_excel(excel_file, index=False)
    print(f"Table {i + 1} saved to {excel_file}")

excel_file = "table_1.xlsx"  
data = pd.read_excel(excel_file)

documents = data.apply(lambda row: " ".join(row.astype(str)), axis=1).tolist()

model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vector_store = Chroma(collection_name="excel_data", embedding_function=embeddings)
vector_store.add_texts(documents)