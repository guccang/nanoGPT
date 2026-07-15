"""
准备唐诗宋词数据集（字符级分词）。
将诗词文本编码为整数序列，保存为 train.bin / val.bin / meta.pkl。

数据格式约定（input.txt 每行一首诗，格式如下）:
标题|作者|正文
示例:
静夜思|李白|床前明月光，疑是地上霜。举头望明月，低头思故乡。

使用方法:
1. 准备 input.txt（每行一首诗，用|分隔标题、作者、正文）
2. python data/poetry_char/prepare.py
"""
import os
import pickle
import numpy as np

# -----------------------------------------------------------------------------
# 1. 读取数据
# -----------------------------------------------------------------------------
input_file_path = os.path.join(os.path.dirname(__file__), 'input.txt')

if not os.path.exists(input_file_path):
    raise FileNotFoundError(
        f"未找到 {input_file_path}\n"
        "请先准备诗词数据文件，每行一首诗，格式: 标题|作者|正文\n"
        "数据来源推荐:\n"
        "  - 全唐诗: https://github.com/chinese-poetry/chinese-poetry\n"
        "  - 或自行整理文本"
    )

with open(input_file_path, 'r', encoding='utf-8') as f:
    data = f.read()

print(f"文本总长度（字符）: {len(data):,}")

# -----------------------------------------------------------------------------
# 2. 构建字符级词表
# -----------------------------------------------------------------------------
chars = sorted(list(set(data)))
vocab_size = len(chars)
print(f"词表内容: {''.join(chars)}")
print(f"词表大小: {vocab_size:,}")

# 建立 字符↔整数 映射
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

def encode(s):
    return [stoi[c] for c in s]

def decode(l):
    return ''.join([itos[i] for i in l])

# -----------------------------------------------------------------------------
# 3. 划分训练/验证集
# -----------------------------------------------------------------------------
n = len(data)
train_data = data[:int(n * 0.9)]
val_data = data[int(n * 0.9):]

train_ids = encode(train_data)
val_ids = encode(val_data)

print(f"训练集 token 数: {len(train_ids):,}")
print(f"验证集 token 数: {len(val_ids):,}")

# -----------------------------------------------------------------------------
# 4. 保存为二进制文件
# -----------------------------------------------------------------------------
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

# -----------------------------------------------------------------------------
# 5. 保存元信息（词表 + 编解码器）
# -----------------------------------------------------------------------------
meta = {
    'vocab_size': vocab_size,
    'itos': itos,
    'stoi': stoi,
}
with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
    pickle.dump(meta, f)

print("数据准备完成！")
print(f"  train.bin / val.bin / meta.pkl 已保存到 {os.path.dirname(__file__)}")
