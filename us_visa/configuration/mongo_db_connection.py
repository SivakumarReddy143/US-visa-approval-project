import os
import sys
from us_visa.exception import USvisaException
import pymongo
import certifi
from us_visa.constant import *
from dotenv import load_dotenv
load_dotenv()

ca=certifi.where()

class MongoClient:
    
    client=None
    def __init__(self,database_name=DATABASE_NAME)->None:
        try:
            if MongoClient.client is None:
                mongo_db_url=os.getenv(MONGO_DB_URL)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGO_DB_URL} is not set.")
                MongoClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.client=MongoClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
        except Exception as e:
            raise USvisaException(e,sys)