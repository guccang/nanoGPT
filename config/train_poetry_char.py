# 训练唐诗宋词字符级 GPT 模型
# 适合小数据集，单 GPU 几分钟即可完成

out_dir = 'out-poetry-char'
eval_interval = 250
eval_iters = 200
log_interval = 10

# 数据量小，只在验证损失改善时保存
always_save_checkpoint = False

wandb_log = False
wandb_project = 'poetry'
wandb_run_name = 'mini-gpt-poetry'

# 数据集
dataset = 'poetry_char'
batch_size = 64
block_size = 128  # 诗词通常较短，128 字符够用

# 小模型（根据数据量调整）
n_layer = 6
n_head = 6
n_embd = 384
dropout = 0.2  # 数据量小，加 dropout 防过拟合

# 学习率
learning_rate = 1e-3
max_iters = 5000
lr_decay_iters = 5000
min_lr = 1e-4
beta2 = 0.99

warmup_iters = 100

# CPU 用户取消以下注释
# device = 'cpu'
# compile = False
