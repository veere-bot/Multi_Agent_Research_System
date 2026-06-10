from langchain.tools import tool
import requests # web requests
from tavily import TavilyClient # web searching
from bs4 import BeautifulSoup # web scraping
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool
def web_search(query:str)->str:
    """ search the web for recent and reliable information on a topic.Return the title ,url and snippet"""
    results = tavily.search(query=query,max_results=5)
    out = []
    for r in results['results']:
        out.append(
            f'Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}\n'
        )
    return "\n-----------\n".join(out)

    # return results
print(web_search.invoke('latest news on TVK party election result'))


@tool 
def scrape_url(url:str)->str:
    """ scrape and return clean text content from a given URL for deeper reading"""
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,'html.parser')
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator='',strip=True)[:3000]
    except Exception as e:
        return f'Coudl not scrape url:{str(e)}'


print(scrape_url.invoke('https://variety.com/2026/politics/news/vijay-tvk-tamil-nadu-election-2026-chief-minister-1236737891'))