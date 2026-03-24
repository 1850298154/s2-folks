# Semantic Scholar API 教程总结

> 来源: https://www.semanticscholar.org/product/api/tutorial

---

## 概述

Semantic Scholar 提供三类 API，每类有独立的 Base URL：

| API 类型 | Base URL |
|----------|----------|
| Academic Graph API | `https://api.semanticscholar.org/graph/v1` |
| Recommendations API | `https://api.semanticscholar.org/recommendations/v1` |
| Datasets API | `https://api.semanticscholar.org/datasets/v1` |

---

## 一、Academic Graph API（学术图谱 API）

### 用途

返回论文、论文作者、论文引用和参考文献的详细信息。

### 主要端点

| 端点 | 方法 | 路径 | 用途 |
|------|------|------|------|
| Paper Details | GET | `/paper/{paper_id}` | 获取单篇论文详情 |
| Paper Batch | POST | `/paper/batch` | 批量获取论文详情 |
| Paper Relevance Search | GET | `/paper/search` | 相关性搜索（资源密集，返回更详细作者/引用信息） |
| Paper Bulk Search | GET | `/paper/search/bulk` | 批量搜索（支持排序和特殊语法，推荐使用） |
| Author Details | GET | `/author/{author_id}` | 获取单个作者信息 |
| Author Batch | POST | `/author/batch` | 批量获取作者信息 |

### 使用示例 - Paper Details

```python
import requests

paperId = "649def34f8be52c8b66281af98ae884c09aef38b"
url = f"http://api.semanticscholar.org/graph/v1/paper/{paperId}"

query_params = {"fields": "title,year,abstract,citationCount"}
headers = {"x-api-key": "your_api_key"}

response = requests.get(url, params=query_params, headers=headers)

if response.status_code == 200:
    print(response.json())
```

### 返回示例

```json
{
    "paperId": "649def34f8be52c8b66281af98ae884c09aef38b",
    "title": "Construction of the Literature Graph in Semantic Scholar",
    "abstract": "We describe a deployed scalable system...",
    "year": 2018,
    "citationCount": 365
}
```

### 使用示例 - Paper Bulk Search

```python
import requests
import json

url = "http://api.semanticscholar.org/graph/v1/paper/search/bulk"

query_params = {
    "query": '"generative ai"',
    "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
    "year": "2023-"
}

headers = {"x-api-key": "your_api_key"}
response = requests.get(url, params=query_params, headers=headers).json()

# 分页处理
print(f"Will retrieve an estimated {response['total']} documents")
retrieved = 0

with open("papers.json", "a") as file:
    while True:
        if "data" in response:
            retrieved += len(response["data"])
            print(f"Retrieved {retrieved} papers...")
            for paper in response["data"]:
                print(json.dumps(paper), file=file)
        if "token" not in response:
            break
        response = requests.get(f"{url}&token={response['token']}").json()

print(f"Done! Retrieved {retrieved} papers total")
```

### 常用查询参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `fields` | 指定返回字段 | `title,year,abstract,citationCount,authors` |
| `query` | 搜索关键词 | `"generative ai"` |
| `year` | 年份过滤 | `2023-` (2023年及以后) |
| `publicationTypes` | 出版类型过滤 | `JournalArticle` |
| `openAccessPdf` | 过滤有公开PDF的论文 | `true` |
| `minCitationCount` | 最小引用数 | `10` |
| `fieldsOfStudy` | 研究领域过滤 | `Computer Science` |
| `venue` | 发表场所过滤 | `Nature` |
| `limit`/`offset` | 分页（relevance search） | `limit=10, offset=0` |
| `token` | 分页（bulk search） | 从响应中获取 |

### 可用字段列表

- `title` - 标题
- `abstract` - 摘要
- `year` - 发表年份
- `url` - Semantic Scholar 页面链接
- `citationCount` - 引用数
- `influentialCitationCount` - 有影响力的引用数
- `authors` - 作者列表
- `openAccessPdf` - 开放获取 PDF 链接
- `publicationTypes` - 出版类型
- `publicationDate` - 出版日期
- `publicationVenue` - 出版场所
- `references` - 参考文献
- `citations` - 引用该论文的论文
- `embedding` - 论文嵌入向量
- `tldr` - AI 生成的摘要

### 使用示例 - Author Batch

```python
import requests

url = "https://api.semanticscholar.org/graph/v1/author/batch"

query_params = {"fields": "name,url,paperCount,hIndex,papers"}
data = {"ids": ["2281351310", "2281342663", "2300302076", "2300141520"]}
headers = {"x-api-key": "your_api_key"}

response = requests.post(url, params=query_params, json=data, headers=headers).json()
```

### 返回示例

```json
[
    {
        "authorId": "2281351310",
        "url": "https://www.semanticscholar.org/author/2281351310",
        "name": "Thomas K. F. Chiu",
        "paperCount": 2,
        "hIndex": 1,
        "papers": [
            {
                "paperId": "630642b7040a0c396967e4dab93cf73094fa4f8f",
                "title": "An experiential learning approach to learn AI..."
            }
        ]
    }
]
```

### 搜索语法示例

| 语法 | 说明 | 示例 |
|------|------|------|
| `+` | 必须包含 | `+security` |
| `-` | 排除 | `-privacy` |
| `|` | 或 | `(cloud computing) | virtualization` |
| `""` | 精确短语 | `"red blood cell"` |
| `*` | 通配符前缀 | `fish*` 匹配 fishes, fishtank |
| `~n` | 编辑距离 | `bugs~3` 匹配 buggy, busg |
| `"phrase"~n` | 短语中允许n个词间隔 | `"blue lake"~3` |

示例：
```
((cloud computing) | virtualization) +security -privacy
```
匹配：包含 "cloud" AND "computing" 或 "virtualization"，必须包含 "security"，排除 "privacy"

---

## 二、Recommendations API（推荐 API）

### 用途

基于给定论文推荐相关论文。

### 主要端点

| 端点 | 方法 | 路径 | 用途 |
|------|------|------|------|
| Single Paper Recommendations | GET | `/papers/forpaper/{paper_id}` | 基于单篇种子论文推荐 |
| Multi Paper Recommendations | POST | `/papers` | 基于多篇正/负种子论文推荐 |

### 使用示例 - 多论文推荐

```python
import requests
import json

url = "https://api.semanticscholar.org/recommendations/v1/papers"

query_params = {
    "fields": "title,url,citationCount,authors",
    "limit": "500"
}

data = {
    "positivePaperIds": [
        "02138d6d094d1e7511c157f0b1a3dd4e5b20ebee",
        "018f58247a20ec6b3256fd3119f57980a6f37748"
    ],
    "negativePaperIds": [
        "0045ad0c1e14a4d1f4b011c92eb36b8df63d65bc"
    ]
}

headers = {"x-api-key": "your_api_key"}
response = requests.post(url, params=query_params, json=data, headers=headers).json()

# 按引用数排序
papers = response["recommendedPapers"]
papers.sort(key=lambda paper: paper["citationCount"], reverse=True)

with open('recommended_papers_sorted.json', 'w') as output:
    json.dump(papers, output)
```

### 返回示例

```json
{
    "recommendedPapers": [
        {
            "paperId": "833ff07d2d1be9be7b12e88487d5631c141a2e95",
            "url": "https://www.semanticscholar.org/paper/833ff07d...",
            "title": "Teacher Professional Development on Self-Determination Theory...",
            "citationCount": 24,
            "authors": [
                {"authorId": "2281351310", "name": "Thomas K. F. Chiu"},
                {"authorId": "2281342663", "name": "C. Chai"}
            ]
        }
    ]
}
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `positivePaperIds` | 正向种子论文 ID 列表（推荐类似这些的论文） |
| `negativePaperIds` | 负向种子论文 ID 列表（排除类似这些的论文） |
| `limit` | 返回数量（最大 500） |
| `fields` | 返回字段 |

---

## 三、Datasets API（数据集 API）

### 用途

下载 Semantic Scholar 完整数据集到本地，支持自行托管和自定义查询。

### 主要端点

| 端点 | 方法 | 路径 | 用途 |
|------|------|------|------|
| List Releases | GET | `/release/` | 获取所有发布日期 |
| List Datasets in Release | GET | `/release/{release_id}` | 获取某次发布的数据集列表 |
| Download Dataset | GET | `/release/{release_id}/dataset/{dataset_name}` | 获取数据集下载链接 |
| Incremental Diffs | GET | `/diffs/{start}/to/{end}/{dataset}` | 获取增量更新 |

### Step 1: 获取所有发布日期

```python
import requests

base_url = "https://api.semanticscholar.org/datasets/v1/release/"
response = requests.get(base_url)
print(response.json())
# 返回: ["2023-10-31", "2023-11-14", "2023-11-28", ...]
```

### Step 2: 获取某次发布的数据集列表

```python
base_url = "https://api.semanticscholar.org/datasets/v1/release/"
release_id = "2023-10-31"  # 或 "latest"

response = requests.get(base_url + release_id)
print(response.json())
# 返回该发布包含的所有数据集名称
```

### Step 3: 获取数据集下载链接

```python
import requests

base_url = "https://api.semanticscholar.org/datasets/v1/release/"
api_key = "your_api_key"
headers = {"x-api-key": api_key}

release_id = "2023-10-31"
dataset_name = "papers"

response = requests.get(
    f"{base_url}{release_id}/dataset/{dataset_name}",
    headers=headers
)
print(response.json())
# 返回包含预签名下载链接的响应
```

### 返回内容

- 数据集名称和描述
- README（许可证和使用信息）
- 预签名临时下载链接列表（文件分片）

### 可用数据集

| 数据集名称 | 说明 |
|-----------|------|
| `papers` | 论文数据 |
| `authors` | 作者数据 |
| `abstracts` | 摘要数据 |
| `embeddings` | 嵌入向量（spector） |
| `publication-venues` | 发表场所 |
| `citations` | 引用关系 |
| `references` | 参考文献关系 |
| `s2affiliations` | 机构关联 |

### 增量更新

获取两个版本之间的增量差异，避免重新下载未变化的数据：

```python
import requests

start_release_id = "2023-10-31"
end_release_id = "2023-11-14"
dataset_name = "authors"
api_key = "your_api_key"
headers = {"x-api-key": api_key}

url = f"https://api.semanticscholar.org/datasets/v1/diffs/{start_release_id}/to/{end_release_id}/{dataset_name}"
response = requests.get(url, headers=headers)
diffs = response.json()['diffs']
print(diffs)
```

增量数据包含：
- **update files**: 需要插入或替换的记录（按主键）
- **delete files**: 需要删除的记录

---

## 效率优化建议

### 1. 使用 API Key

- 无 Key 用户共享单一速率限制
- 有 Key 用户获得 1 req/s 的独立配额
- 申请地址: https://www.semanticscholar.org/product/api#api-key

### 2. 使用批量端点

- Paper Bulk Search 代替 Paper Relevance Search
- Paper Batch 代替多次 Paper Details
- Author Batch 代替多次 Author Details

### 3. 限制 fields 参数

只请求需要的字段，减少响应时间。

### 4. 大规模数据使用 Datasets API

当需要高于 API 速率限制的访问时，下载数据集到本地查询。

---

## 分页机制

### limit/offset 分页（Paper Relevance Search）

```python
url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {"query": "halloween", "limit": 3, "offset": 0}
# 偏移量从0开始，下一页 offset=3
```

### token 分页（Paper Bulk Search）

```python
# 首次请求
response = requests.get(url, params=query_params).json()

# 后续请求
while "token" in response:
    response = requests.get(f"{url}&token={response['token']}").json()
```

---

## HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | 请求成功 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未认证或凭证无效 |
| 403 Forbidden | 无权限访问 |
| 404 Not Found | 资源不存在 |
| 429 Too Many Requests | 触发速率限制 |
| 500 Internal Server Error | 服务器内部错误 |

---

## 总结对比

| 特性 | Academic Graph API | Recommendations API | Datasets API |
|------|-------------------|---------------------|--------------|
| 主要用途 | 查询论文/作者/引用信息 | 论文推荐 | 批量下载数据 |
| 请求方式 | GET/POST | GET/POST | GET |
| 需要 API Key | 可选（推荐） | 可选（推荐） | **必需** |
| 数据格式 | JSON 实时返回 | JSON 实时返回 | JSON 文件下载 |
| 适用场景 | 实时查询少量数据 | 发现相关论文 | 大规模数据分析 |
| 速率限制 | 1 req/s（有key） | 1 req/s（有key） | 无实时限制 |
| 数据量 | 单次最多 500 条 | 单次最多 500 条 | 完整数据集 |

---

## 官方资源

- API 文档: https://api.semanticscholar.org/api-docs/
- Postman 集合: https://www.postman.com/science-operator-43364886/workspace/semantic-scholar-examples
- GitHub 示例: https://github.com/allenai/s2-folks/tree/main/examples
- Slack 社区: https://join.slack.com/t/semanticschol-xyj3882
