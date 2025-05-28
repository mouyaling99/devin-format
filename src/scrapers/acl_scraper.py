import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from ..models.paper import Paper

class ACLScraper:
    def __init__(self):
        self.base_url = "https://aclanthology.org"
    
    def scrape_recent_papers(self, year: int = None) -> List[Paper]:
        if year is None:
            year = datetime.now().year
        
        venues = ['acl', 'emnlp', 'naacl', 'eacl', 'coling']
        papers = []
        
        for venue in venues:
            venue_url = f"{self.base_url}/venues/{venue}/"
            response = requests.get(venue_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paper_links = soup.find_all('a', href=True)
                for link in paper_links:
                    if f"{year}" in link['href'] and 'pdf' not in link['href']:
                        paper_url = self.base_url + link['href']
                        paper = self._scrape_paper_details(paper_url, venue)
                        if paper and self._is_llm_related(paper):
                            papers.append(paper)
        
        return papers
    
    def _scrape_paper_details(self, paper_url: str, venue: str) -> Paper:
        """Scrape details of a specific paper"""
        try:
            response = requests.get(paper_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title_elem = soup.find('h2', class_='card-title')
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                authors = []
                author_elems = soup.find_all('span', class_='author')
                for author in author_elems:
                    authors.append(author.text.strip())
                
                abstract_elem = soup.find('div', class_='card-body acl-abstract')
                abstract = abstract_elem.text.strip() if abstract_elem else ""
                
                pdf_link = None
                pdf_elem = soup.find('a', text='PDF')
                if pdf_elem and 'href' in pdf_elem.attrs:
                    pdf_link = self.base_url + pdf_elem['href']
                
                year_str = paper_url.split('/')[-2] if '/' in paper_url else str(datetime.now().year)
                try:
                    year = int(year_str)
                    pub_date = datetime(year, 1, 1)  # Default to January 1st of the year
                except ValueError:
                    pub_date = datetime.now()
                
                return Paper(
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    url=paper_url,
                    pdf_url=pdf_link,
                    published_date=pub_date,
                    source='acl',
                    venue=venue.upper(),
                    citation_count=None,
                    categories=['Computational Linguistics']
                )
        except Exception as e:
            print(f"Error scraping paper details from {paper_url}: {e}")
        
        return None
    
    def _is_llm_related(self, paper: Paper) -> bool:
        """Check if paper is related to LLMs based on title and abstract"""
        llm_keywords = [
            "language model", "LLM", "transformer", "GPT", "BERT", 
            "model evaluation", "data construction", "benchmark", "dataset"
        ]
        
        text = (paper.title + " " + paper.abstract).lower()
        return any(keyword.lower() in text for keyword in llm_keywords)
