from logging_config import logger
from model_setup import llm_model_conn,embd_model_conn
from database import database_connection

##Document 
from langchain_community.document_loaders import TextLoader
try:
    logger.info("1st Phase Start :Data Load")
    docs=TextLoader("Project/external.txt",encoding="utf-8")
    docs=docs.load()
    logger.info("1st Phase Complete : Data Load")

except Exception as e:
    logger.info("1st Phase  Failed :%s",e)

##Spliting
from langchain_text_splitters import RecursiveCharacterTextSplitter
try:
    logger.info("2nd Phase Start :Data Spliting")
    rec_obj=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunk=rec_obj.split_documents(docs)
    logger.info("2nd Phase Complete :Data Spliting")

except Exception as e:
    logger.info("2nd Phase Failed :%s",e)


##Embedding
emb_model=embd_model_conn()
conn=database_connection()

for i in chunk:
    chunks=i.page_content
    embedding=emb_model.embed_query(chunks)

    query="""
          insert into "Rudra"."clg_document"("content","embedding")
          values(%s,%s)"""

    cur=conn.cursor()
    cur.execute(query,(chunks,embedding))


conn.commit()
cur.close()
conn.close()

logger.info("Embedding Store Succesfully :")