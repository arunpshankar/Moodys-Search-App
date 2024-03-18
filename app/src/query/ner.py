from src.query.sematic_search import find_closest_match
from src.config.logging import logger
from src.generate.llm import LLM
from typing import Dict


llm = LLM()


def extract_entities(query: str) -> Dict[str, str]:
    """
    Extract key entities from the given query.

    Args:
    query (str): The input query from which information is to be extracted.

    Returns:
    Dict[str, str]: A dictionary containing extracted entities like company name, country, report type, year, and URLs.
    """
    logger.info("Starting Named Entity Recognition (NER)")
    extracted_entities = {}
    
    def extract_entity(task: str, query: str) -> str:
        return llm.predict(task=task, query=query)

    extracted_entities['company'] = extract_entity('Given a query as shown below, extract the company name from it. If company name not found return NONE.', query)
    extracted_entities['country'] = extract_entity('Given a query as shown below, extract the country name from it. If country name not found return NONE.', query)
    extracted_entities['report_type'] = extract_entity('Given a query as shown below, extract the report type from it. If report type not found return NONE.', query)
    extracted_entities['year'] = extract_entity('Given a query as shown below, extract the year from it. If year not found return NONE.', query)
    
    closest_match = find_closest_match(extracted_entities['company'])
    extracted_entities['company'] = closest_match.get('bank_name', 'NONE')
    extracted_entities['site_url'] = closest_match.get('site_url', 'NONE')

    if extracted_entities['country'] == 'NONE':
        extracted_entities['country'] = closest_match.get('country', 'NONE')

    logger.info("NER completed successfully!")
    return extracted_entities


if __name__ == '__main__':
    query = "Annual Report 2012 commerzbank"
    entities = extract_entities(query)
    logger.info(entities)
