import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from logging_config import logger

def database_connection():
    logger.info("Database Connection Start :")
    try:
         conn=psycopg2.connect(
              host=os.getenv("DB_HOST"),
              user=os.getenv("DB_USER"),
              database=os.getenv("DB_NAME"),
              password=os.getenv("DB_PASSWORD"),
              port=os.getenv("DB_PORT")

         )
         logger.info("Database Connection Succesfull :")
         return conn

    except Exception as e:
         logger.info("Database Connection Failed %s",e)