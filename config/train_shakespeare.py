# 从头训练莎士比亚 BPE 模型（tiktoken gpt2 分词）
# 词表大小 50,257，数据约 301,966 tokens

out_dir = 'out-shakespeare'
eval_interval = 250
eval_iters = 200
log_interval = 10

always_save_checkpoint = False

wandb_log = False
wandb_project = 'shakespeare'
wandb_run_name = 'shakespeare-bpe'

dataset = 'shakespeare'
gradient_accumulation_steps = 1
batch_size = 12
block_size = 1024

# 模型配置
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.2

# 优化器
learning_rate = 1e-3
max_iters = 5000
lr_decay_iters = 5000
min_lr = 1e-4
beta2 = 0.99

warmup_iters = 100
