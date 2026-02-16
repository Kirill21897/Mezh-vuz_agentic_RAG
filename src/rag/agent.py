import logging
from typing import Dict, Any, List
from src.rag.retriever import HybridRetriever
from src.rag.schema import RAGResponse, SearchResult

logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self):
        self.retriever = HybridRetriever()

    def _parse_query(self, query: str) -> Dict[str, Any]:
        """
        Simulates an LLM parsing the query to extract filters.
        In a real scenario, this would call an LLM with function calling.
        """
        filters = {}
        query_lower = query.lower()
        
        # Simple heuristic extraction
        if "москв" in query_lower:
            filters["city"] = "Москва"
        if "питер" in query_lower or "санкт-петербург" in query_lower:
            filters["city"] = "Санкт-Петербург"
        if "бакалавр" in query_lower:
            filters["level"] = "бакалавриат"
        if "магистр" in query_lower:
            filters["level"] = "магистратура"
            
        return filters

    def _generate_answer(self, query: str, results: List[SearchResult]) -> str:
        """
        Simulates an LLM generating an answer from results.
        """
        if not results:
            return "К сожалению, я не нашел подходящих программ по вашему запросу."
            
        answer = f"По вашему запросу '{query}' найдено {len(results)} программ:\n\n"
        
        for i, res in enumerate(results, 1):
            prog = res.metadata.get('name_prog', 'Неизвестная программа')
            univ = res.metadata.get('name_univ', 'Неизвестный ВУЗ')
            city = res.metadata.get('city', 'Неизвестный город')
            answer += f"{i}. **{prog}** в {univ} ({city})\n"
            # Extract a snippet from content if description is not available or too long
            desc = res.metadata.get('description_prog', '')
            if not desc:
                 desc = res.content
            
            snippet = desc[:200] + "..." if len(desc) > 200 else desc
            answer += f"   {snippet}\n\n"
            
        return answer

    def process_query(self, query: str) -> RAGResponse:
        """
        Main entry point for the agent.
        1. Parse query -> filters
        2. Retrieve documents
        3. Generate answer
        """
        logger.info(f"Processing query: {query}")
        
        # 1. Plan/Parse
        filters = self._parse_query(query)
        logger.info(f"Extracted filters: {filters}")
        
        # 2. Retrieve
        results = self.retriever.search(query, filters=filters)
        logger.info(f"Found {len(results)} results")
        
        # 3. Generate
        answer = self._generate_answer(query, results)
        
        return RAGResponse(answer=answer, sources=results)
