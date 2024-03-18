from src.search.site_search import extract_relevant_data as site_search_extract
from src.search.cdn_search import extract_relevant_data as cdn_search_extract
from src.search.site_search import search_data_store as site_search
from src.search.cdn_search import search_data_store as cdn_search
from src.db.match import find_entity_url_by_key
from src.query.ner import extract_entities
from src.config.logging import logger
from typing import Dict 


def perform_search(query_mode: str, query: str):
    """
    Perform a specific type of search based on the query mode and the incoming user query.

    Parameters:
    query_mode (str): Mode of query ('Raw' or 'Reformulated').
    query (str): The search query.

    Returns:
    dict: A dictionary of dictionaries containing search results.
    """
    results = {}
    entities = extract_entities(query)
    logger.info(f'Extracted Entities: {entities}')
    company = entities['company']
    report_type = entities['report_type']
    country = entities['country']
    year = entities['year']
    site_url = entities['site_url']
    entities = {'company': company, 'report_type': report_type, 'country': country, 'year': year, 'site_url': site_url}
    
    logger.info(f'Starting Vertex AI Search with Query Mode: <{query_mode}>')

    row_info = find_entity_url_by_key(company, country)
    if row_info:
        batch_id = row_info['batch_id'] 
    
        if query_mode == 'Raw':
            response = site_search(query, batch_id=batch_id)
            results['site'] = site_search_extract(response)
            response = cdn_search(search_query=query)
            results['cdn'] = cdn_search_extract(response)
        elif query_mode == 'Targeted':
            reformulated_query = f'filetype:pdf "{company}" {year} {report_type} {country} {site_url}'
            response = site_search(reformulated_query, batch_id)
            results['site'] = site_search_extract(response)
            results['reformulated_query_site_search'] = reformulated_query
            reformulated_query = f'filetype:pdf "{company}" {year} {report_type} {country}'
            response = cdn_search(search_query=reformulated_query)
            results['cdn'] = cdn_search_extract(response)
            results['reformulated_query_cdn_search'] = reformulated_query

    logger.info('Vertex AI Search completed')
    logger.info(results)
    return results, entities


if __name__ == "__main__":
    query = "Musashino Bank Annual Report 2021 Japan"
    matches = perform_search(query_mode="Reformulated", query=query)
    logger.info(matches)