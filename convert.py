python
import requests

# 1. 原始链接
source_url = "https://github.com/qwerttvv/Beijing-IPTV/releases/download/iptv/IPTV-Unicom-Multicast.m3u"
# 2. 如果你有 udpxy 需求，把下面换成你的内网地址，如果没有，就写 "rtp://" 保持原样
target_prefix = "http://192.168.1.1:8686/rtp/" 

def main():
    try:
        r = requests.get(source_url, timeout=30)
        r.encoding = 'utf-8'
        # 批量替换地址
        modified_data = r.text.replace("rtp://", target_prefix)
        
        # 你可以在这里加更多修改逻辑，比如改组名等
        # modified_data = modified_data.replace('group-title="央视频道"', 'group-title="我的央视"')

        with open("beijing.m3u", "w", encoding="utf-8") as f:
            f.write(modified_data)
        print("处理成功！")
    except Exception as e:
        print(f"处理失败: {e}")

if __name__ == "__main__":
    main()
