from langchain_community.document_loaders import JSONLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.config.logging import logger 
from src.config.setup import config
from typing import Dict



def extract_metadata(record: Dict, metadata: Dict) -> Dict:
    """
    Extract necessary metadata from a record.
    
    Parameters:
    record (Dict): Record from which to extract metadata.
    metadata (Dict): Metadata dictionary to update.

    Returns:
    Dict: Updated metadata dictionary.
    """
    metadata['url'] = record.get('url', 'Unknown')
    metadata['country'] = record.get('country', 'Unknown')
    return metadata



def load_and_index(file_path: str) -> FAISS:
    logger.info(f"Starting to load data from {file_path}")
    loader = JSONLoader(file_path=file_path,
                        jq_schema='.',
                        metadata_func=extract_metadata,
                        content_key='entity',
                        json_lines=True)
    
    entities = loader.load()
    logger.info("Data loaded successfully")

    logger.info("Initializing text embedder")
    text_embedder = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
    text_embedder.instance['batch_size'] = 100
    logger.info("Text embedder initialized")
    logger.info(text_embedder.instance)

    logger.info("Creating FAISS vector store from loaded data")
    vector_store = FAISS.from_documents(entities, text_embedder)
    logger.info("FAISS vector store created successfully")

    return vector_store






if __name__ == "__main__":
    vector_store = load_and_index("./data/entities.jsonl")
    vector_store.save_local("./data/faiss_index/")