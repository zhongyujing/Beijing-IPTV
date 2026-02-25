import requests

# 1. 原始链接
source_url = "https://github.com/qwerttvv/Beijing-IPTV/releases/download/iptv/IPTV-Unicom-Multicast.m3u"
# 2. 播放地址前缀（按需修改）
target_prefix = "http://192.168.1.1:8686/rtp/" 

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        
        # 将获取到的内容按行分割
        lines = r.text.split('\n')
        new_lines = []
        
        skip_next = False  # 用于标记是否需要跳过下一行（即播放地址行）

        for line in lines:
            # 如果上一行触发了删除逻辑，跳过这一行（地址行）
            if skip_next:
                skip_next = False
                continue

            # 核心逻辑 1：检查是否是频道信息行
            if line.startswith("#EXTINF") or line.startswith("# #EXTINF"):
                # 检查是否包含“超清”或“HDR”
                if "超清" in line or "HDR" in line:
                    skip_next = True  # 标记下一行（地址行）也要删除
                    continue          # 跳过当前行（信息行）
                
                # 核心逻辑 2：修正格式，将 "# #EXTINF" 改为 "#EXTINF"
                line = line.replace("# #EXTINF", "#EXTINF")
            
            # 核心逻辑 3：如果是播放地址行，修改前缀
            if line.startswith("rtp://"):
                line = line.replace("rtp://", target_prefix)

            # 将没被删掉的行加入新列表
            new_lines.append(line)

        # 将处理后的行重新组合并保存
        with open("beijing.m3u", "w", encoding="utf-8") as f:
            f.write('\n'.join(new_lines))
        
        print("处理成功：已删除超清/HDR频道，并修正了 #EXTINF 格式。")

    except Exception as e:
        print(f"处理失败: {e}")
        exit(1)

if __name__ == "__main__":
    main()
