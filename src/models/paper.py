from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Paper:
    title: str
    authors: List[str]
    abstract: str
    url: str
    pdf_url: Optional[str]
    published_date: datetime
    source: str  # arxiv, acl, neurips, etc.
    venue: Optional[str]
    citation_count: Optional[int]
    categories: List[str]
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'url': self.url,
            'pdf_url': self.pdf_url,
            'published_date': self.published_date.isoformat(),
            'source': self.source,
            'venue': self.venue,
            'citation_count': self.citation_count,
            'categories': self.categories
        }
