from typing import List, Dict, Any
from ..models.paper import Paper

class QualityFilter:
    """Filter papers based on quality criteria"""
    
    def __init__(self):
        self.prestigious_venues = [
            'ACL', 'EMNLP', 'NAACL', 'EACL', 'COLING',  # NLP conferences
            'NeurIPS', 'ICML', 'ICLR', 'AAAI', 'IJCAI',  # ML conferences
            'TACL', 'CL', 'JMLR', 'TPAMI'  # Journals
        ]
        
        self.prestigious_orgs = [
            'google', 'microsoft', 'meta', 'facebook', 'openai', 'anthropic',
            'deepmind', 'ai2', 'stanford', 'mit', 'berkeley', 'cmu', 
            'oxford', 'cambridge', 'tsinghua', 'peking', 'eth zurich'
        ]
        
        self.influential_researchers = [
            'yoshua bengio', 'yann lecun', 'geoffrey hinton', 
            'ilya sutskever', 'sam altman', 'dario amodei',
            'jacob devlin', 'ashish vaswani', 'alec radford',
            'tom brown', 'percy liang', 'christopher manning',
            'graham neubig', 'kyunghyun cho', 'jason weston'
        ]
    
    def filter_papers(self, papers: List[Paper]) -> List[Paper]:
        """Filter papers based on quality criteria"""
        high_quality_papers = []
        
        for paper in papers:
            quality_score = self._calculate_quality_score(paper)
            if quality_score >= 1:  # Threshold for high-quality papers
                high_quality_papers.append(paper)
        
        return high_quality_papers
    
    def _calculate_quality_score(self, paper: Paper) -> float:
        """Calculate quality score for a paper based on various criteria"""
        score = 0.0
        
        if paper.venue and any(venue.lower() in paper.venue.lower() for venue in self.prestigious_venues):
            score += 1.0
        
        author_text = ' '.join(paper.authors).lower()
        for org in self.prestigious_orgs:
            if org in author_text:
                score += 0.5
                break
        
        for researcher in self.influential_researchers:
            if researcher.lower() in author_text:
                score += 1.0
                break
        
        if paper.citation_count:
            if paper.citation_count >= 100:
                score += 1.0
            elif paper.citation_count >= 50:
                score += 0.5
            elif paper.citation_count >= 10:
                score += 0.2
        
        if paper.source == 'arxiv' and paper.categories:
            relevant_categories = ['cs.CL', 'cs.AI', 'cs.LG']
            if any(cat in paper.categories for cat in relevant_categories):
                score += 0.3
        
        return score
