import requests
from bs4 import BeautifulSoup
import threading
import matplotlib.pyplot as plt
import pandas as pd

# 設定 PTT Stock 版的 URL
base_url = 'https://www.ptt.cc/bbs/Stock/index.html'

# 設定 headers，避免被網站反爬機制封鎖
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# 發送 GET 請求
def fetch_page(url):
    """爬取單一頁面的文章標題"""
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析文章標題
    articles = soup.find_all('div', class_='title')
    article_titles = []
    for article in articles:
        a_tag = article.find('a')
        if a_tag:
            article_titles.append(a_tag.text.strip())
            print(f"- {a_tag.text.strip()} (Link: https://www.ptt.cc{a_tag['href']})")
    return soup, article_titles

def get_next_page_url(soup):
    """獲取下一頁的 URL"""
    next_page = soup.find('a', string='‹ 上頁')
    if next_page:
        return 'https://www.ptt.cc' + next_page['href']
    return None

def crawl_all_pages(url, max_pages=10):
    """爬取指定頁數的文章"""
    page_count = 0
    all_article_titles = []
    while url and page_count < max_pages:
        print(f"Processing {url}...")
        soup, articles = fetch_page(url)
        all_article_titles.extend(articles)
        url = get_next_page_url(soup)  # 確保使用最新的 soup 來獲取下一頁 URL
        page_count += 1
    return all_article_titles

# 開始爬取 PTT Stock 版的文章，設定最多爬取 10 頁
print("Starting to crawl PTT Stock board...")
all_titles = crawl_all_pages(base_url, max_pages=10)

# 資料分析與視覺化（假設我們已經爬取到標題資料並放入 DataFrame）
def analyze_and_visualize_title_lengths(articles):
    """分析標題長度分佈並視覺化"""
    df = pd.DataFrame(articles, columns=['title'])

    # 取得標題長度
    df['title_length'] = df['title'].apply(len)

    # 顯示標題長度的分佈
    plt.hist(df['title_length'], bins=30, edgecolor='black')
    plt.title('Distribution of Article Title Lengths')
    plt.xlabel('Title Length')
    plt.ylabel('Frequency')
    
    # 顯示圖片
    plt.show()

# 調用視覺化方法
analyze_and_visualize_title_lengths(all_titles)
