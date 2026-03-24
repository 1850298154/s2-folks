"""搜索反思相关的Agent顶会论文"""
import os
import time
import requests

S2_API_KEY = os.getenv('S2_API_KEY')

# 顶级会议列表
TOP_VENUES = [
    'NeurIPS', 'ICML', 'ICLR', 'ACL', 'AAAI', 'IJCAI',
    'EMNLP', 'NAACL', 'CVPR', 'ICCV', 'ECCV',
    'COLING', 'AAMAS', 'KDD', 'WWW', 'SIGIR'
]

def search_papers(query, limit=20):
    """搜索论文"""
    rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/search',
                       headers={'X-API-KEY': S2_API_KEY},
                       params={
                           'query': query,
                           'limit': limit,
                           'fields': 'title,url,year,venue,citationCount,authors'
                       })
    rsp.raise_for_status()
    return rsp.json()

def is_top_venue(venue):
    """检查是否为顶级会议"""
    if not venue:
        return False
    venue_upper = venue.upper()
    return any(top in venue_upper for top in TOP_VENUES)

def main():
    # 搜索关键词 - 使用更精确的查询
    queries = [
        'reflection agent reasoning',
        'self-reflection LLM agent'
    ]

    all_papers = []

    for query in queries:
        print(f"\n搜索: {query}")
        try:
            results = search_papers(query, limit=20)

            if 'data' in results:
                for paper in results['data']:
                    venue = paper.get('venue', '')
                    if is_top_venue(venue):
                        all_papers.append(paper)

            time.sleep(3)  # 添加延迟避免速率限制
        except Exception as e:
            print(f"搜索出错: {e}")
            continue

    # 去重（按paperId）
    seen = set()
    unique_papers = []
    for paper in all_papers:
        if paper['paperId'] not in seen:
            seen.add(paper['paperId'])
            unique_papers.append(paper)

    # 按引用数排序
    unique_papers.sort(key=lambda x: x.get('citationCount', 0), reverse=True)

    print(f"\n{'='*80}")
    print(f"找到 {len(unique_papers)} 篇反思相关的Agent顶会论文:")
    print('='*80)

    for i, paper in enumerate(unique_papers[:20], 1):
        title = paper.get('title', 'N/A')
        venue = paper.get('venue', 'N/A')
        year = paper.get('year', 'N/A')
        citations = paper.get('citationCount', 0)
        url = paper.get('url', '')
        authors = paper.get('authors', [])
        first_author = authors[0]['name'] if authors else 'Unknown'

        print(f"\n{i}. {title}")
        print(f"   作者: {first_author} et al. | 会议: {venue} ({year}) | 引用: {citations}")
        print(f"   链接: {url}")

if __name__ == '__main__':
    main()
