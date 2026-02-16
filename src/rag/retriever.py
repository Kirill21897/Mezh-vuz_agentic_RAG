import pandas as pd
import logging
from typing import List, Optional, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.core.data_loader import DataLoader
from src.rag.schema import SearchResult

logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self):
        self.loader = DataLoader()
        # Get data
        try:
            self.df = self.loader.get_merged_active_programs().reset_index(drop=True)
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            self.df = pd.DataFrame()

        self.vectorizer = None
        self.tfidf_matrix = None
        
        if not self.df.empty:
            self._prepare_search_index()

    def _prepare_search_index(self):
        # Create a text field for search
        # Combine name, description, requirements, university name, city
        self.df['search_text'] = (
            self.df['name_prog'].fillna('') + " " + 
            self.df['description_prog'].fillna('') + " " + 
            self.df['requirements'].fillna('') + " " +
            self.df['name_univ'].fillna('') + " " +
            self.df['city'].fillna('')
        ).astype(str)

        # Initialize TF-IDF
        self.vectorizer = TfidfVectorizer() 
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['search_text'])
        logger.info(f"Initialized TF-IDF index with {self.tfidf_matrix.shape[0]} documents.")

    def search(self, query: str, filters: Optional[Dict[str, Any]] = None, top_k: int = 5) -> List[SearchResult]:
        if self.df.empty or self.vectorizer is None:
            logger.warning("Search index is empty.")
            return []

        # 1. Text Search Score
        try:
            query_vec = self.vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            self.df['score'] = scores
        except Exception as e:
            logger.error(f"Error during vector search: {e}")
            return []

        # 2. Apply Filters (Structured Search)
        filtered_df = self.df.copy()
        
        if filters:
            for key, value in filters.items():
                if key in filtered_df.columns and value:
                    # If string, use case-insensitive contains
                    if isinstance(value, str):
                        filtered_df = filtered_df[filtered_df[key].astype(str).str.contains(value, case=False, na=False)]
                    # If list, use isin
                    elif isinstance(value, list):
                        filtered_df = filtered_df[filtered_df[key].isin(value)]
                    # Exact match for others
                    else:
                        filtered_df = filtered_df[filtered_df[key] == value]

        if filtered_df.empty:
            return []

        # 3. Sort by score
        result_df = filtered_df.sort_values(by='score', ascending=False).head(top_k)
        
        results = []
        for _, row in result_df.iterrows():
            # Format content for display
            content = f"""
            Программа: {row['name_prog']}
            ВУЗ: {row['name_univ']}
            Город: {row['city']}
            Описание: {row['description_prog']}
            Требования: {row['requirements']}
            """
            
            # Convert row to dict for metadata, handle NaN
            metadata = row.where(pd.notnull(row), None).to_dict()
            
            results.append(SearchResult(
                content=content.strip(),
                metadata=metadata,
                score=float(row['score'])
            ))
            
        return results
