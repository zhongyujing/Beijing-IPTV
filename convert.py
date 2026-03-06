import requests
import os

# 1. 原始链接
source_url = "https://raw.githubusercontent.com/zzzz0317/beijing-unicom-iptv-playlist/refs/heads/main/iptv-multicast.m3u"
# 2. 你的内网 udpxy 地址前缀
target_prefix = "http://192.168.1.1:8686/rtp/" 

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        print(f"正在从源获取数据: {source_url}")
        r = requests.get(source_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        
        lines = r.text.split('\n')
        new_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 核心逻辑 1：处理频道信息行（仅修正格式，不再过滤关键词）
            if line.startswith("#EXTINF") or line.startswith("# #EXTINF"):
                # 修正格式：将 "# #EXTINF" 统一改为标准 "#EXTINF"
                line = line.replace("# #EXTINF", "#EXTINF")
            
            # 核心逻辑 2：处理播放地址行（深度修复：去除开头的 # 和 空格）
            # 逻辑：如果行中包含 rtp:// 且不是以标准 #EXT 开头的描述行
            elif "rtp://" in line and not line.startswith("#EXT"):
                # 先把开头的 # 号和可能存在的空格通通删掉，还原成标准的 rtp://...
                if line.startswith("#"):
                    line = line.lstrip("#").strip()
                
                # 统一修改前缀为你的 udpxy 地址
                if line.startswith("rtp://"):
                    line = line.replace("rtp://", target_prefix)

            new_lines.append(line)

        # 写入文件
        file_name = "Beijing-IPTV.m3u"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write('\n'.join(new_lines))
        
        print(f"处理成功！已保留所有频道（含超清/HDR/8K），并修复了地址行。")

    except Exception as e:
        print(f"处理失败: {e}")
        exit(1)

if __name__ == "__main__":
    main()
