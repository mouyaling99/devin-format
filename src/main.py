#!/usr/bin/env python3
import argparse
import os
from datetime import datetime, timedelta
from src.scrapers.arxiv_scraper import ArxivScraper
from src.scrapers.acl_scraper import ACLScraper
from src.scrapers.pwc_scraper import PWCScraper
from src.utils.storage import PaperStorage
from src.utils.quality_filter import QualityFilter

def main():
    parser = argparse.ArgumentParser(description='LLM Paper Collector - 收集和整理大模型相关高质量论文')
    parser.add_argument('--days', type=int, default=7, help='Days to look back (查询过去几天的论文)')
    parser.add_argument('--search', type=str, help='Search query (搜索关键词)')
    parser.add_argument('--field', type=str, default='all',
                        choices=['title', 'abstract', 'authors', 'all'],
                        help='Field to search in (搜索的字段: 标题/摘要/作者/全部)')
    parser.add_argument('--date', type=str, help='Specific date to load papers from (YYYY-MM-DD) (加载特定日期的论文)')
    parser.add_argument('--date-range', type=str, nargs=2, metavar=('START_DATE', 'END_DATE'),
                        help='Date range to filter papers (YYYY-MM-DD) (按日期范围过滤论文)')

    args = parser.parse_args()

    os.makedirs('data', exist_ok=True)

    storage = PaperStorage()

    if args.search:
        results = storage.search_papers(args.search, args.field)
        print(f"Found {len(results)} papers matching '{args.search}' in field '{args.field}'")
        for i, paper in enumerate(results, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'])}")
            print(f"   Date: {paper['published_date']}")
            print(f"   Source: {paper['source']}")
            print(f"   URL: {paper['url']}")

    elif args.date:
        papers = storage.load_papers(args.date)
        print(f"Loaded {len(papers)} papers from {args.date}")
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'])}")
            print(f"   Source: {paper['source']}")

    elif args.date_range:
        try:
            start_date = datetime.fromisoformat(args.date_range[0])
            end_date = datetime.fromisoformat(args.date_range[1])
            papers = storage.get_papers_by_date_range(start_date, end_date)
            print(f"Found {len(papers)} papers between {args.date_range[0]} and {args.date_range[1]}")
            for i, paper in enumerate(papers, 1):
                print(f"\n{i}. {paper['title']}")
                print(f"   Date: {paper['published_date']}")
                print(f"   Source: {paper['source']}")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    else:
        print("Collecting new papers...")

        scrapers = [
            ArxivScraper(),
            ACLScraper(),
            PWCScraper()
        ]

        all_papers = []
        for scraper in scrapers:
            scraper_name = scraper.__class__.__name__
            print(f"Scraping from {scraper_name}...")
            if scraper_name == "ACLScraper":
                papers = scraper.scrape_recent_papers(year=datetime.now().year)
            else:
                papers = scraper.scrape_recent_papers(days=args.days)
            # papers = scraper.scrape_recent_papers(days=args.days)
            print(f"  Found {len(papers)} papers")
            all_papers.extend(papers)

        print(f"Total papers collected: {len(all_papers)}")

        print("Filtering for high-quality papers...")
        quality_filter = QualityFilter()
        high_quality_papers = quality_filter.filter_papers(all_papers)

        print(f"High-quality papers: {len(high_quality_papers)}")

        if high_quality_papers:
            storage.save_papers(high_quality_papers)
            print(f"Saved {len(high_quality_papers)} papers to data directory")

            print("\nSummary of collected papers:")
            for i, paper in enumerate(high_quality_papers[:10], 1):  # Show top 10
                print(f"\n{i}. {paper.title}")
                print(f"   Authors: {', '.join(paper.authors[:3])}" +
                      (f" and {len(paper.authors) - 3} more" if len(paper.authors) > 3 else ""))
                print(f"   Source: {paper.source}")
                print(f"   URL: {paper.url}")

            if len(high_quality_papers) > 10:
                print(f"\n... and {len(high_quality_papers) - 10} more papers")
        else:
            print("No high-quality papers found in the specified time period.")

if __name__ == "__main__":
    main()
