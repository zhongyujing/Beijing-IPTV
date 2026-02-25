import requests

# 1. 原始链接
source_url = "https://github.com/qwerttvv/Beijing-IPTV/releases/download/iptv/IPTV-Unicom-Multicast.m3u"
# 2. 播放地址前缀（按需修改，如果不改就保持 "rtp://"）
target_prefix = "http://192.168.1.1:8686/rtp/" 

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        
        lines = r.text.split('\n')
        new_lines = []
        skip_next = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 如果上一行是需要删除的频道（超清/HDR/8K），跳过这一行
            if skip_next:
                skip_next = False
                continue

            # 核心逻辑 1：处理频道信息行
            if line.startswith("#EXTINF") or line.startswith("# #EXTINF"):
                # 关键词过滤：超清、HDR、8K
                if any(word in line for word in ["超清", "HDR", "8K"]):
                    skip_next = True
                    continue
                
                # 修正格式：将 "# #EXTINF" 统一改为 "#EXTINF"
                line = line.replace("# #EXTINF", "#EXTINF")
            
            # 核心逻辑 2：处理播放地址行（深度修复：去除开头的 # 和 空格）
            # 如果这一行包含 rtp:// 且不是以标准 #EXT 开头的描述行
            if "rtp://" in line and not line.startswith("#EXT"):
                # 先把开头的 # 和 空格通通删掉，还原成标准的 rtp://...
                if line.startswith("#"):
                    line = line.lstrip("#").strip()
                
                # 统一修改前缀为你的 udpxy 地址
                if line.startswith("rtp://"):
                    line = line.replace("rtp://", target_prefix)

            new_lines.append(line)

        # 写入文件
        with open("Beijing-IPTV.m3u", "w", encoding="utf-8") as f:
            f.write('\n'.join(new_lines))
        
        print("处理成功：已删除【超清/HDR/8K】频道，修复了信息行格式，并去除了地址前的多余 # 号。")

    except Exception as e:
        print(f"处理失败: {e}")
        exit(1)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
