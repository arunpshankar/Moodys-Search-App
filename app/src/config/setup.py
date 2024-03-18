from google.auth.transport.requests import Request
from google.oauth2 import service_account
from src.config.logging import logger
from typing import Dict
from typing import Any
import subprocess
import yaml
import os

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            # The following line ensures that the __init__ method is only called once.
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = "./config/config.yml"):
        """
        Initialize the Config class.

        Args:
        - config_path (str): Path to the YAML configuration file.
        """
        if self.__initialized:
            return
        self.__initialized = True
        
        self.__config = self._load_config(config_path)
        self.PROJECT_ID = self.__config['project_id']
        self.REGION = self.__config['region']
        self.CREDENTIALS_PATH = self.__config['credentials_json']
        self._set_google_credentials(self.CREDENTIALS_PATH)
        self.ACCESS_TOKEN = self._set_access_token()
        self.CDN_SEARCH_DATA_STORE_ID = self.__config['cdn_search_datastore_id']
        self.TEXT_EMBED_MODEL_NAME = self.__config['text_embed_model_name']
        self.TEXT_GEN_MODEL_NAME = self.__config['text_gen_model_name']

        self.BUCKET = self.__config['bucket']
        self.CLOUD_SQL_INSTANCE = self.__config['cloud_sql_instance']
        self.CLOUD_SQL_USERNAME = self.__config['cloud_sql_username']
        self.CLOUD_SQL_PASSWORD = self.__config['cloud_sql_password']
        self.CLOUD_SQL_DATABASE = self.__config['cloud_sql_database']
        self.CLOUD_SQL_USERS_TABLE = self.__config['cloud_sql_users_table']
        self.CLOUD_SQL_FEEDBACK_TABLE = self.__config['cloud_sql_feedback_table']
        self.CLOUD_SQL_URLS_TABLE = self.__config['cloud_sql_urls_table']

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        """
        Load the YAML configuration from the given path.

        Args:
        - config_path (str): Path to the YAML configuration file.

        Returns:
        - dict: Loaded configuration data.
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load the configuration file. Error: {e}")
    

    @staticmethod
    def _set_access_token() -> str:
        """
        Fetch an access token for authentication using the Google Cloud SDK for Python.

        Returns:
        - str: The fetched access token.
        """
        logger.info("Fetching access token...")
        try:
            # Path to your service account key file
            key_path = "path/to/your/service-account-file.json"
            
            # Load the credentials from the service account file
            credentials = service_account.Credentials.from_service_account_file(
                key_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            # Request a new token if needed
            if not credentials.valid or credentials.expired:
                credentials.refresh(Request())

            logger.info("Access token obtained successfully.")
            return credentials.token
        except Exception as e:
            logger.error(f"Failed to fetch access token. Error: {e}")
            return ""

    


config = Config()