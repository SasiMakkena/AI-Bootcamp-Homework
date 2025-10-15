"""
MinSearch index helpers: build and query.
"""
from typing import List, Dict, Any
from minsearch import Index


def build_index(docs: List[Dict[str, Any]],
                text_fields: List[str],
                keyword_fields: List[str]) -> Index:
    """
    Build a MinSearch index over the given documents.
    """
    index = Index(text_fields=text_fields, keyword_fields=keyword_fields)
    index.fit(docs)
    return index


def search_index(index: Index, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Query the MinSearch index, returning top-k results.
    """
    if not isinstance(query, str):
        raise TypeError(f"Query must be a string, got {type(query)}")
    return index.search(query=query, num_results=num_results)
