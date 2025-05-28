import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional
from ..models.paper import Paper

class PWCScraper:
    """Papers With Code scraper for LLM-related papers"""
    
    def __init__(self):
        self.base_url = "https://paperswithcode.com"
        self.nlp_url = f"{self.base_url}/area/natural-language-processing"
        self.llm_topics = [
            "language-modelling", "large-language-models", 
            "transformer", "gpt", "bert", "llm"
        ]
    
    def scrape_recent_papers(self, days: int = 30) -> List[Paper]:
        """Scrape recent papers from Papers With Code"""
        papers = []
        
        papers.extend(self._scrape_from_url(self.nlp_url))
        
        for topic in self.llm_topics:
            topic_url = f"{self.base_url}/task/{topic}"
            papers.extend(self._scrape_from_url(topic_url))
        
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        recent_papers = [p for p in papers if p.published_date >= cutoff_date]
        
        return self._deduplicate_papers(recent_papers)
    
    def _scrape_from_url(self, url: str) -> List[Paper]:
        """Scrape papers from a specific URL"""
        papers = []
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                paper_cards = soup.find_all('div', class_='paper-card')
                
                for card in paper_cards:
                    paper = self._extract_paper_from_card(card)
                    if paper:
                        papers.append(paper)
        except Exception as e:
            print(f"Error scraping from {url}: {e}")
        
        return papers
    
    def _extract_paper_from_card(self, card) -> Optional[Paper]:
        """Extract paper information from a paper card element"""
        try:
            title_elem = card.find('h1')
            if not title_elem:
                return None
                
            title = title_elem.text.strip()
            
            url_elem = card.find('a', href=True)
            if not url_elem:
                return None
                
            paper_url = self.base_url + url_elem['href'] if url_elem['href'].startswith('/') else url_elem['href']
            
            authors = []
            author_elems = card.find_all('a', class_='author-name')
            for author in author_elems:
                authors.append(author.text.strip())
            
            abstract_elem = card.find('p', class_='paper-abstract')
            abstract = abstract_elem.text.strip() if abstract_elem else ""
            
            date_elem = card.find('span', class_='date')
            pub_date = datetime.now()
            if date_elem:
                date_text = date_elem.text.strip()
                try:
                    pub_date = datetime.strptime(date_text, "%d %b %Y")
                except ValueError:
                    pass
            
            pdf_url = None
            pdf_elem = card.find('a', text='PDF')
            if pdf_elem and 'href' in pdf_elem.attrs:
                pdf_url = pdf_elem['href']
            
            citation_count = None
            citation_elem = card.find('span', class_='citation-number')
            if citation_elem:
                try:
                    citation_count = int(citation_elem.text.strip())
                except ValueError:
                    pass
            
            return Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                url=paper_url,
                pdf_url=pdf_url,
                published_date=pub_date,
                source='paperswithcode',
                venue=None,
                citation_count=citation_count,
                categories=['Natural Language Processing']
            )
        except Exception as e:
            print(f"Error extracting paper from card: {e}")
            return None
    
    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on title and URL"""
        unique_papers = {}
        for paper in papers:
            if paper.url not in unique_papers:
                unique_papers[paper.url] = paper
        
        return list(unique_papers.values())
