import requests
import os

# 原始链接
source_url = "https://github.com/qwerttvv/Beijing-IPTV/releases/download/iptv/IPTV-Unicom-Multicast.m3u"
# 你的前缀（根据需要修改，如果不改就保持 "rtp://"）
target_prefix = "http://192.168.1.1:8686/rtp/" 

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        print(f"正在下载: {source_url}")
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status() # 如果下载失败会抛出异常
        r.encoding = 'utf-8'
        
        # 核心替换逻辑
        content = r.text
        if "rtp://" in content:
            modified_data = content.replace("rtp://", target_prefix)
            with open("beijing.m3u", "w", encoding="utf-8") as f:
                f.write(modified_data)
            print("文件处理成功，已保存为 beijing.m3u")
        else:
            print("警告：原始文件中未发现 rtp:// 地址，请检查源文件内容。")
            
    except Exception as e:
        print(f"发生错误: {e}")
        exit(1) # 告诉 GitHub Actions 运行失败

if __name__ == "__main__":
    main()
