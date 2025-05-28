import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models.paper import Paper

class PaperStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_papers(self, papers: List[Paper]) -> None:
        """Save papers to a JSON file organized by date"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.data_dir, f"papers_{today}.json")
        
        paper_dicts = [paper.to_dict() for paper in papers]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(paper_dicts, f, indent=2, ensure_ascii=False)
    
    def load_papers(self, date_str: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load papers from a specific date or all papers if date is None"""
        if date_str:
            filename = os.path.join(self.data_dir, f"papers_{date_str}.json")
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        else:
            return self._load_all_papers()
    
    def _load_all_papers(self) -> List[Dict[str, Any]]:
        """Load all papers from all JSON files"""
        all_papers = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("papers_") and filename.endswith(".json"):
                file_path = os.path.join(self.data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                    all_papers.extend(papers)
        return all_papers
    
    def search_papers(self, query: str, field: str = "all") -> List[Dict[str, Any]]:
        """Search papers by query in specified field"""
        all_papers = self._load_all_papers()
        results = []
        
        for paper in all_papers:
            if self._matches_query(paper, query, field):
                results.append(paper)
        
        return results
    
    def _matches_query(self, paper: Dict[str, Any], query: str, field: str) -> bool:
        """Check if paper matches the query in the specified field"""
        query = query.lower()
        
        if field == "title":
            return query in paper['title'].lower()
        elif field == "abstract":
            return query in paper['abstract'].lower()
        elif field == "authors":
            return any(query in author.lower() for author in paper['authors'])
        else:  # "all" or any other value
            if query in paper['title'].lower():
                return True
            if query in paper['abstract'].lower():
                return True
            if any(query in author.lower() for author in paper['authors']):
                return True
        
        return False
    
    def get_papers_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get papers published within a date range"""
        all_papers = self._load_all_papers()
        results = []
        
        for paper in all_papers:
            try:
                pub_date = datetime.fromisoformat(paper['published_date'])
                if start_date <= pub_date <= end_date:
                    results.append(paper)
            except (ValueError, KeyError):
                continue
        
        return results
