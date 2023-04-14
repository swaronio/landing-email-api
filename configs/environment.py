import os, dotenv

class Environment:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    @staticmethod
    def load_environment():
        dotenv.load_dotenv()
        Environment.update_environment()
        
    def update_environment():
        Environment.DB_USER = os.getenv('DB_USER')
        Environment.DB_PASSWORD = os.getenv('DB_PASSWORD')
        Environment.DB_HOST = os.getenv('DB_HOST')
        Environment.DB_PORT = os.getenv('DB_PORT')
        Environment.DB_NAME = os.getenv('DB_NAME')