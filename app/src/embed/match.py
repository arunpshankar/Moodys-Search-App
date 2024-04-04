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


def format_matches(matches: List[Dict[str, Any]]) -> str:
    """
    Formats a list of match dictionaries into a human-friendly string representation with line breaks between attributes.

    Parameters:
    - matches (List[Dict[str, Any]]): The matches to format.

    Returns:
    - str: A string representation of the matches with line breaks.
    """
    formatted_matches = []
    for match in matches:
        formatted_match = (
            f"company: {match['company']}\n"
            f"url: {match['url']}\n"
            f"country: {match['country']}\n"
        )
        formatted_matches.append(formatted_match)
        formatted_matches.append('-' * 50)

    # Join all formatted matches with an extra line break for separation
    return '\n'.join(formatted_matches)


if __name__ == "__main__":
    text_embedder = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
    text_embedder.instance['batch_size'] = 100

    question = "hsbc bank"

    vector_store = FAISS.load_local("./data/faiss_index/", text_embedder, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    matches_by_title = match_by_country(question, retriever)

   
    print("Matches by Company Name:")
    print(format_matches(matches_by_title))
