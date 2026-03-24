"""搜索经典反思Agent论文 - 使用bulk API"""
import requests
import json
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

# 顶级会议
TOP_VENUES = [
    'NeurIPS', 'ICML', 'ICLR', 'ACL', 'AAAI', 'IJCAI',
    'EMNLP', 'NAACL'
]

def is_top_venue(venue):
    if not venue:
        return False
    venue_upper = venue.upper()
    return any(top in venue_upper for top in TOP_VENUES)

def search_bulk(query):
    fields = "title,year,venue,url,citationCount,authors"
    url = f"http://api.semanticscholar.org/graph/v1/paper/search/bulk?query={query}&fields={fields}"
    try:
        r = requests.get(url, timeout=30).json()
        return r
    except Exception as e:
        print(f"搜索出错: {e}")
        return {}

# 经典论文关键词
queries = [
    "Reflexion language agent verbal reinforcement",
    "ReAct reasoning acting language model",
    "Tree of Thoughts deliberate problem solving",
    "Self-Refine iterative refinement self-feedback",
    "Chain of Thought prompting reasoning",
    "Self-consistency language model reasoning",
]

all_papers = []

for query in queries:
    print(f"搜索: {query}")
    r = search_bulk(query)
    if "data" in r:
        for paper in r["data"]:
            venue = paper.get('venue', '')
            citations = paper.get('citationCount', 0)
            if is_top_venue(venue) or citations > 100:
                all_papers.append(paper)
    time.sleep(1)

# 去重
seen = set()
unique_papers = []
for paper in all_papers:
    if paper['paperId'] not in seen:
        seen.add(paper['paperId'])
        unique_papers.append(paper)

# 按引用数排序
unique_papers.sort(key=lambda x: x.get('citationCount', 0), reverse=True)

print(f"\n{'='*80}")
print(f"经典反思/推理相关Agent论文 ({len(unique_papers)} 篇):")
print('='*80)

for i, paper in enumerate(unique_papers[:20], 1):
    title = paper.get('title', 'N/A')
    venue = paper.get('venue', 'N/A')
    year = paper.get('year', 'N/A')
    citations = paper.get('citationCount', 0)
    url_link = paper.get('url', '')
    authors = paper.get('authors', [])
    first_author = authors[0]['name'] if authors else 'Unknown'

    print(f"\n{i}. {title}")
    print(f"   作者: {first_author} et al. | 会议: {venue} ({year}) | 引用: {citations}")
    print(f"   链接: {url_link}")
