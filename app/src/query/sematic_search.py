from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import VertexAIEmbeddings
from src.config.logging import logger
from src.config.setup import config
from typing import List 
from typing import Dict 


def execute_query(query: str, retriever):
    """
    Execute a query and log the resulting documents.
    
    Parameters:
    query (str): Query string.
    retriever: Retriever object for document retrieval.
    """
    logger.info(f"Executing query: {query}")
    matches = []
    try:
        banks = retriever.get_relevant_documents(query)
        for bank in banks:
            name = bank.page_content
            metadata = bank.metadata
            country = metadata['country']
            site_url = metadata['site_url']
            matches.append({'bank_name': name, 'country': country, 'site_url': site_url})
        logger.info(f"Query executed successfully")
    except Exception as e:
        logger.error(f"Error executing query '{query}': {e}")
    return matches


def find_closest_match(query: str) -> List[Dict]:
    embeddings = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
    vector_store = FAISS.load_local("./data/faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    matches = execute_query(query, retriever)
    return matches[0]


if __name__ == "__main__":
    match = find_closest_match('commerzbank')
    print(match)