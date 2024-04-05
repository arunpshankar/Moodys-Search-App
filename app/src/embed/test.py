from typing import List, Dict, Tuple
import json
from tqdm import tqdm
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.embed.match import match_by_country
from src.config.logging import logger
from src.config.setup import config


# Setup the text embedder
text_embedder = VertexAIEmbeddings(model_name=config.TEXT_EMBED_MODEL_NAME)
text_embedder.instance['batch_size'] = 100

# Load the vector store
vector_store = FAISS.load_local("./data/faiss_index/", text_embedder, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 1})


def test_name_resolution(filepath: str) -> List[bool]:
    """Test name resolution for various entity name variants.

    Args:
        filepath (str): Path to the test data file containing JSONL formatted entity variants.

    Returns:
        List[bool]: A list of boolean values indicating the success or failure of each test.
    """
    results = []
    with open(filepath, 'r') as file:
        for line in tqdm(file, desc="Processing test cases"):
            data = json.loads(line)
            variants = data['variants']
            for variant in variants:
                top_match = match_by_country(variant, retriever)
                expected = data['entity']  
                success = top_match[0]['company'] == expected
                results.append(success)
                if not success:
                    logger.info(f"Failed: Expected company name = {expected} | Resolved company name = {top_match[0]['company']}")

    success_rate = sum(results) / len(results) * 100
    logger.info(f"Success Rate: {success_rate:.2f}%")

# Path to your test data file
test_data_path = './data/test_entities.jsonl'
test_name_resolution(test_data_path)