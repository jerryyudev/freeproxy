import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 获取代理列表
def fetch_proxies(url):
    response = requests.get(url)
    proxies = [line.strip() for line in response.text.splitlines() if line.strip()]
    return proxies

# 检查代理是否有效
def check_proxy(proxy):
    try:
        response = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            return proxy, True
    except requests.RequestException:
        return proxy, False
    return proxy, False

# 主程序
def main():
    url = "https://mf.botnet.dog/ccc.txt"  # 代理源文件 URL
    proxies_list = fetch_proxies(url)  # 获取代理列表
    working_proxies = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有代理检查任务
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies_list}
        
        for future in as_completed(future_to_proxy):
            proxy, is_working = future.result()
            if is_working:
                print(f"代理 {proxy} 可用！")
                working_proxies.append(proxy)

    # 输出测试结束
    print("代理检测结束。")

# 运行主程序
if __name__ == "__main__":
    main()
