import requests
import feedparser
from datetime import datetime, timedelta
from typing import List
from ..models.paper import Paper

class ArxivScraper:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.llm_keywords = [
            "large language model", "LLM", "language model",
            "transformer", "GPT", "BERT", "model evaluation",
            "data construction", "benchmark", "dataset"
        ]
    
    def scrape_recent_papers(self, days: int = 7) -> List[Paper]:
        papers = []
        for keyword in self.llm_keywords:
            query = f'search_query=all:"{keyword}"&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending'
            
            response = requests.get(f"{self.base_url}?{query}")
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                pub_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
                if pub_date >= datetime.now() - timedelta(days=days):
                    paper = Paper(
                        title=entry.title,
                        authors=[author.name for author in entry.authors],
                        abstract=entry.summary,
                        url=entry.link,
                        pdf_url=entry.link.replace('abs', 'pdf'),
                        published_date=pub_date,
                        source='arxiv',
                        venue='arXiv',
                        citation_count=None,
                        categories=[tag.term for tag in entry.tags]
                    )
                    papers.append(paper)
        
        return self._deduplicate_papers(papers)
    
    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on title and URL"""
        unique_papers = {}
        for paper in papers:
            if paper.url not in unique_papers:
                unique_papers[paper.url] = paper
        
        return list(unique_papers.values())
