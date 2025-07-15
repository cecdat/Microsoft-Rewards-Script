import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

def scrape_baidu_hot():
    """
    抓取百度实时热搜榜，并将结果覆盖写入到文件中。
    """
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在执行抓取任务...")
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        hot_items = soup.find_all('div', class_='c-single-text-ellipsis')

        if not hot_items:
            print("错误：未能找到热搜词条。可能是百度页面结构已更新。")
            return

        search_terms = [item.get_text(strip=True) for item in hot_items]

        file_name = 'search_terms.txt'
        
        # 使用 'w' 模式打开文件，这会在写入前自动清空文件内容
        with open(file_name, 'w', encoding='utf-8') as f:
            for term in search_terms:
                f.write(term + '\n')
        
        print(f"成功抓取 {len(search_terms)} 个热搜词，并已覆盖写入到 {file_name} 文件中。")

    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

if __name__ == "__main__":
    # 立即执行一次
    scrape_baidu_hot()
    
    # 设置定时任务，每小时执行一次
    schedule.every(1).hour.do(scrape_baidu_hot)
    
    print("计划任务已启动，将每小时抓取一次百度热搜并覆盖保存。")
    print("请保持此窗口运行，按 Ctrl+C 可以停止。")

    while True:
        schedule.run_pending()
        time.sleep(1)
