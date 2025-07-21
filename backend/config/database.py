from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    _client = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        if self._client is None:
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('MONGODB_DATABASE')
            
            try:
                self._client = MongoClient(mongodb_uri)
                self._database = self._client[database_name]
                # 測試連接
                self._client.admin.command('ping')
                print(f"Successfully connected to MongoDB: {database_name}")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise e
    
    def get_database(self):
        if self._database is None:
            self.connect()
        return self._database
    
    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]
    
    def close_connection(self):
        if self._client:
            self._client.close()
            self._client = None
            self._database = None

# 全域資料庫實例
db = Database()
