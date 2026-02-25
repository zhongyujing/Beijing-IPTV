import requests

# 1. 原始链接
source_url = "https://github.com"
# 2. 你的内网 udpxy 地址前缀
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
            # 跳过空行
            if not line:
                continue

            # 如果上一行触发了删除标记（超清/HDR/8K），跳过当前的地址行
            if skip_next:
                skip_next = False
                continue

            # 逻辑 1：处理频道信息行
            if line.startswith("#EXTINF") or line.startswith("# #EXTINF"):
                # 关键词过滤：删除包含 超清、HDR、8K 的频道
                if any(word in line for word in ["超清", "HDR", "8K"]):
                    skip_next = True
                    continue
                
                # 格式修正：将 "# #EXTINF" 统一改为标准 "#EXTINF"
                line = line.replace("# #EXTINF", "#EXTINF")
            
            # 逻辑 2：处理地址行（去掉多余 # 并转换前缀）
            # 先去掉可能存在的开头多余 # 号（如 #rtp://）
            if line.startswith("#rtp://"):
                line = line[1:]
            
            # 将 rtp:// 统一替换为你的 http://192.168.1.1:8686/rtp/
            if line.startswith("rtp://"):
                line = line.replace("rtp://", target_prefix)

            new_lines.append(line)

        # 写入结果文件
        with open("beijing.m3u", "w", encoding="utf-8") as f:
            f.write('\n'.join(new_lines))
        
        print(f"处理成功：已剔除无用频道，并转换地址为 {target_prefix}")

    except Exception as e:
        print(f"执行出错: {e}")
        exit(1)

if __name__ == "__main__":
    main()
