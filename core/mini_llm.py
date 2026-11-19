import math

# 1. 最极简的 Tokenizer (把字符映射成数字)
class CharTokenizer:
    def __init__(self, text):
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}

    def encode(self, text):
        return [self.stoi.get(c, 0) for c in text]

    def decode(self, tokens):
        return "".join([self.itos.get(t, '?') for t in tokens])

# 2. 搭建底层神经网络（手搓矩阵乘和注意力）
class MiniAttention:
    def __init__(self, embed_size):
        self.embed_size = embed_size

    def forward(self, x):
        # 极其简化的 Self-Attention 概念演示
        # 实际大模型里这里会有 Wq, Wk, Wv 矩阵乘法
        scores = [[sum(a * b for a, b in zip(row1, row2)) for row2 in x] for row1 in x]
        
        # Softmax 归一化 (算概率)
        exp_scores = [[math.exp(s) for s in row] for row in scores]
        sum_exp = [sum(row) for row in exp_scores]
        attn_weights = [[exp_scores[i][j] / sum_exp[i] for j in range(len(x))] for i in range(len(x))]
        
        # 加权求和
        output = []
        for i in range(len(x)):
            out_vec = [sum(attn_weights[i][j] * x[j][k] for j in range(len(x))) for k in range(self.embed_size)]
            output.append(out_vec)
        return output, attn_weights

# 3. 测试我们的底层大模型引擎
if __name__ == "__main__":
    text = "hello llm"
    tokenizer = CharTokenizer(text)
    tokens = tokenizer.encode("hello")
    print(f"原始文本: 'hello'")
    print(f"词汇表大小: {tokenizer.vocab_size}")
    print(f"Token 编码: {tokens}")

    # 模拟 Embedding（把数字变成 4 维向量）
    # 真实模型有几万维
    embed_size = 4
    embeddings = [[float(t) + i * 0.1 for i in range(embed_size)] for t in tokens]
    print(f"\n词向量 (Embeddings): {embeddings}")

    # 跑一次 Attention
    attention = MiniAttention(embed_size)
    output, weights = attention.forward(embeddings)
    print(f"\n注意力权重 (Attention Weights):")
    for row in weights:
        print(["%.2f" % w for w in row])
        
    print(f"\n大模型底层计算完成！这就是黑魔法的本质。")