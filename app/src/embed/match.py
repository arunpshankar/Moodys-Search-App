from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.config.logging import logger
from src.config.setup import config
from typing import List, Dict, Any


def match_by_country(query: str, retriever: Any) -> List[Dict[str, Any]]:
    logger.info(f"Executing title query: '{query}'")
    matches = []
    try:
        docs = retriever.get_relevant_documents(query)
        for doc in docs:
            match = {
                'url': doc.metadata['url'],
                'company': doc.page_content,
                'country': doc.metadata['country']
            }
            matches.append(match)
    except Exception as e:
        logger.error(f"Error during title query execution: {e}")
    return matches

if __name__ == "__main__":
    text_embedder = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
    text_embedder.instance['batch_size'] = 100

    question = "Nextracker, Inc"

    vector_store = FAISS.load_local("./data/faiss_index/", text_embedder, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 1})
    matches_by_title = match_by_country(question, retriever)
    print(matches_by_title[0])
