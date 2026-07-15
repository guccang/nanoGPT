"""
将 chinese-poetry 仓库的 JSON 数据转换为 nanoGPT 训练用的 input.txt 格式。
每行一首诗，格式: 标题|作者|正文
所有文本统一转换为简体中文。

数据来源: https://github.com/chinese-poetry/chinese-poetry
"""
import os
import json
import glob
from opencc import OpenCC

# 繁体转简体
cc = OpenCC('t2s')

# chinese-poetry 仓库路径（克隆到 /tmp/chinese-poetry）
REPO_PATH = '/tmp/chinese-poetry'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

total_count = 0

with open(OUTPUT_PATH, 'w', encoding='utf-8') as out:

    # ============================================================
    # 1. 全唐诗 (poet.tang.*.json)
    # ============================================================
    tang_files = sorted(glob.glob(os.path.join(REPO_PATH, '全唐诗', 'poet.tang.*.json')))
    print(f"找到 {len(tang_files)} 个唐诗文件")
    tang_count = 0
    for fpath in tang_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            poems = json.load(f)
        for poem in poems:
            author = poem.get('author', '佚名')
            title = poem.get('title', '无题')
            # paragraphs 是列表，每个元素是一联，用句号分隔
            paragraphs = poem.get('paragraphs', [])
            if not paragraphs:
                continue
            # 将各联拼接为一个字符串
            content = ''.join(paragraphs)
            # 清理内容中的换行符
            content = content.replace('\n', '').replace('\r', '')
            # 繁体转简体
            title = cc.convert(title)
            author = cc.convert(author)
            content = cc.convert(content)
            line = f"{title}|{author}|{content}\n"
            out.write(line)
            tang_count += 1
    print(f"唐诗写入: {tang_count} 首")
    total_count += tang_count

    # ============================================================
    # 2. 全宋诗 (poet.song.*.json)
    # ============================================================
    song_files = sorted(glob.glob(os.path.join(REPO_PATH, '全唐诗', 'poet.song.*.json')))
    print(f"找到 {len(song_files)} 个宋诗文件")
    song_count = 0
    for fpath in song_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            poems = json.load(f)
        for poem in poems:
            author = poem.get('author', '佚名')
            title = poem.get('title', '无题')
            paragraphs = poem.get('paragraphs', [])
            if not paragraphs:
                continue
            content = ''.join(paragraphs)
            content = content.replace('\n', '').replace('\r', '')
            # 繁体转简体
            title = cc.convert(title)
            author = cc.convert(author)
            content = cc.convert(content)
            line = f"{title}|{author}|{content}\n"
            out.write(line)
            song_count += 1
    print(f"宋诗写入: {song_count} 首")
    total_count += song_count

    # ============================================================
    # 3. 宋词 (ci.song.*.json)
    # ============================================================
    ci_files = sorted(glob.glob(os.path.join(REPO_PATH, '宋词', 'ci.song.*.json')))
    print(f"找到 {len(ci_files)} 个宋词文件")
    ci_count = 0
    for fpath in ci_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            poems = json.load(f)
        for poem in poems:
            author = poem.get('author', '佚名')
            # 宋词用 rhythmic（词牌名）作为标题
            title = poem.get('rhythmic', '无题')
            paragraphs = poem.get('paragraphs', [])
            if not paragraphs:
                continue
            content = ''.join(paragraphs)
            content = content.replace('\n', '').replace('\r', '')
            # 繁体转简体
            title = cc.convert(title)
            author = cc.convert(author)
            content = cc.convert(content)
            line = f"{title}|{author}|{content}\n"
            out.write(line)
            ci_count += 1
    print(f"宋词写入: {ci_count} 首")
    total_count += ci_count

print(f"\n总计写入: {total_count} 首")
print(f"输出文件: {OUTPUT_PATH}")
