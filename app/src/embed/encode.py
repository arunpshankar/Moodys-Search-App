from langchain_community.document_loaders import JSONLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.config.logging import logger
from src.config.setup import config
from typing import Dict



def extract_metadata(record: Dict[str, any], metadata: Dict[str, str]) -> Dict[str, str]:
    """
    Extracts necessary metadata from a given record and updates the metadata dictionary.

    Parameters:
        record (Dict[str, any]): A dictionary representing the record from which to extract metadata.
        metadata (Dict[str, str]): A dictionary where the extracted metadata will be updated.

    Returns:
        Dict[str, str]: The updated metadata dictionary containing information extracted from the record.
    """
    metadata['url'] = record.get('url', 'Unknown')
    metadata['country'] = record.get('country', 'Unknown')
    return metadata

def load_and_index(file_path: str) -> FAISS:
    """
    Loads data from a JSON lines file, indexes it using VertexAI for embeddings, and creates a FAISS vector store.

    Parameters:
        file_path (str): The path to the JSON lines file containing the data to be indexed.

    Returns:
        FAISS: A FAISS vector store object containing the indexed data.
    """
    logger.info(f"Starting to load data from {file_path}")

    loader = JSONLoader(
        file_path=file_path,
        jq_schema='.',
        metadata_func=extract_metadata,
        content_key='entity',
        json_lines=True
    )

    entities = loader.load()
    logger.info("Data loaded successfully")

    logger.info("Initializing text embedder with model name from configuration")
    text_embedder = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
    text_embedder.instance['batch_size'] = 100  # Batch size for embedding processing
    logger.info("Text embedder initialized with configuration: %s", text_embedder.instance)

    logger.info("Creating FAISS vector store from loaded data")
    vector_store = FAISS.from_documents(documents=entities, embedder=text_embedder)
    logger.info("FAISS vector store created successfully")

    return vector_store

if __name__ == "__main__":
    vector_store = load_and_index("./data/entities.jsonl")
    vector_store.save_local("./data/faiss_index/")
    logger.info("FAISS vector store saved locally to './data/faiss_index/'")
