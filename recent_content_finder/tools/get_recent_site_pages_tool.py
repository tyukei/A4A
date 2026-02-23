from google.adk.tools.function_tool import FunctionTool

def get_recent_site_pages(base_url: str) -> str:
    \"\"\"指定されたURLのサイト内から、過去3ヶ月以内に公開・更新されたページを最大100件リストアップします。
    
    Args:
        base_url: 調査対象のサイトのベースURL（例: https://example.com）
        
    Returns:
        タイトル、URL、公開/更新日のリスト（マークダウン形式）
    \"\"\"
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime, timedelta
    from urllib.parse import urljoin, urlparse
    import json
    import re

    # 3ヶ月前の日付を計算
    three_months_ago = datetime.now() - timedelta(days=90)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse_date(date_str):
        if not date_str: return None
        try:
            # ISO形式 (2023-10-27T...) または YYYY-MM-DD
            return datetime.fromisoformat(date_str[:10].replace('/', '-'))
        except:
            return None

    def get_sitemap_urls(url):
        parsed_url = urlparse(url)
        base = f\"{parsed_url.scheme}://{parsed_url.netloc}\"
        sitemaps = []
        
        # 1. robots.txtから探す
        try:
            robots_res = requests.get(urljoin(base, \"/robots.txt\"), headers=headers, timeout=5)
            if robots_res.status_code == 200:
                for line in robots_res.text.split('\\n'):
                    if line.lower().startswith('sitemap:'):
                        sitemaps.append(line.split(':', 1)[1].strip())
        except:
            pass
        
        # 2. デフォルトパスを追加
        if not sitemaps:
            sitemaps.append(urljoin(base, \"/sitemap.xml\"))
            
        return list(set(sitemaps))

    def parse_sitemap(sitemap_url, depth=0):
        if depth > 2: return [] # 再帰の制限
        urls_with_dates = []
        try:
            res = requests.get(sitemap_url, headers=headers, timeout=10)
            if res.status_code != 200: return []
            
            soup = BeautifulSoup(res.content, 'xml')
            
            # sitemapindexの場合（子サイトマップを辿る）
            for sitemap in soup.find_all('sitemap'):
                loc = sitemap.find('loc')
                if loc:
                    urls_with_dates.extend(parse_sitemap(loc.text, depth + 1))
            
            # urlsetの場合
            for url_tag in soup.find_all('url'):
                loc = url_tag.find('loc')
                lastmod = url_tag.find('lastmod')
                if loc:
                    urls_with_dates.append({
                        'url': loc.text, 
                        'date': parse_date(lastmod.text) if lastmod else None
                    })
        except:
            pass
        return urls_with_dates

    def extract_info_from_html(url):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200: return None
            
            soup = BeautifulSoup(res.content, 'html.parser')
            title = (soup.title.string.strip() if soup.title else url) or url
            
            date_found = None
            
            # 1. JSON-LDからの抽出
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        d = item.get('datePublished') or item.get('dateModified') or item.get('uploadDate')
                        if d:
                            date_found = parse_date(d)
                            break
                    if date_found: break
                except:
                    continue
            
            # 2. Metaタグからの抽出
            if not date_found:
                meta_tags = [
                    {'property': 'article:published_time'},
                    {'property': 'og:updated_time'},
                    {'name': 'pubdate'},
                    {'name': 'date'},
                    {'property': 'og:published_time'}
                ]
                for tag_attr in meta_tags:
                    tag = soup.find('meta', attrs=tag_attr)
                    if tag and tag.get('content'):
                        date_found = parse_date(tag.get('content'))
                        if date_found: break
            
            return {'title': title, 'url': url, 'date': date_found}
        except:
            return None

    # メイン実行
    sitemaps = get_sitemap_urls(base_url)
    candidates = []
    for s in sitemaps:
        candidates.extend(parse_sitemap(s))
    
    # 重複排除
    seen_urls = set()
    unique_candidates = []
    for c in candidates:
        if c['url'] not in seen_urls:
            unique_candidates.append(c)
            seen_urls.add(c['url'])
    
    recent_results = []
    checked_count = 0
    
    # まずはsitemapで日付が3ヶ月以内のものを優先チェック
    for c in unique_candidates:
        if checked_count >= 100: break
        if c['date'] and c['date'] >= three_months_ago:
            info = extract_info_from_html(c['url'])
            if info and info['date'] and info['date'] >= three_months_ago:
                recent_results.append(info)
            checked_count += 1

    # 日付不明なものを残りの枠でチェック
    if checked_count < 100:
        for c in unique_candidates:
            if checked_count >= 100: break
            if not c['date']:
                info = extract_info_from_html(c['url'])
                if info and info['date'] and info['date'] >= three_months_ago:
                    recent_results.append(info)
                checked_count += 1

    if not recent_results:
        return f\"{base_url} 内に過去3ヶ月以内の更新ページは見つかりませんでした（最大100ページ確認）。\"
    
    # 出力の整形
    output = f\"### {base_url} の過去3ヶ月以内の更新・公開ページ（最大100件調査結果）\\n\\n\"
    # 日付順にソート
    recent_results.sort(key=lambda x: x['date'] or datetime.min, reverse=True)
    
    for page in recent_results:
        d_str = page['date'].strftime('%Y-%m-%d') if page['date'] else \"不明\"
        output += f\"- **[{page['title']}]({page['url']})**\\n  - 公開/更新日: {d_str}\\n\"
        
    return output


# FunctionToolとして登録
get_recent_site_pages_tool = FunctionTool(func=get_recent_site_pages)
