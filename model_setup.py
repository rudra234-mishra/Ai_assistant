import os
from dotenv import load_dotenv
load_dotenv()
from logging_config import logger
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings

##llm Model
def llm_model_conn():
    logger.info("Model Connection Start :")
    try:
         llm_model=AzureChatOpenAI(
              api_key=os.getenv("AZURE_OPENAI_API_KEY"),
              api_version=os.getenv("api_version"),
              azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
              model=os.getenv("AZURE_OPENAI_MODEL"),
              max_completion_tokens=250,
              temperature=0.3
         )
         logger.info("Model Connection Succesfull :")
         return llm_model

    except Exception as e:
         logger.info("Model Connection Failed %s",e)


##Embedding Model
def embd_model_conn():
     logger.info("Embedding Model Connection Start :")
     try:
          embd_model=AzureOpenAIEmbeddings(
               api_key=os.getenv("AZURE_OPENAI_API_KEY"),
               api_version=os.getenv("api_version"),
               azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
               azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
          )
          logger.info("Embedding Model Connection Succesfull :")
          return embd_model
     
     except Exception as e:
          logger.info("Embedding Model Connection Failed %s",e)