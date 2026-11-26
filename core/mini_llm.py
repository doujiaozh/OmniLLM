# -*- coding: utf-8 -*-
import math


class CharTokenizer:
    def __init__(self, text):
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}

    def encode(self, text):
        return [self.stoi.get(c, 0) for c in text]


class MiniAttention:
    def __init__(self, embed_size):
        self.embed_size = embed_size

    def forward(self, x):
        scores = [[sum(a * b for a, b in zip(row1, row2)) for row2 in x] for row1 in x]
        exp_scores = [[math.exp(s) for s in row] for row in scores]
        sum_exp = [sum(row) for row in exp_scores]
        attn_weights = [
            [exp_scores[i][j] / sum_exp[i] for j in range(len(x))]
            for i in range(len(x))
        ]

        output = []
        for i in range(len(x)):
            out_vec = [
                sum(attn_weights[i][j] * x[j][k] for j in range(len(x)))
                for k in range(self.embed_size)
            ]
            output.append(out_vec)
        return output, attn_weights


if __name__ == "__main__":
    tokenizer = CharTokenizer("hello llm")
    tokens = tokenizer.encode("hello")
    print("Raw: 'hello'")
    print("Tokens:", tokens)

    embed_size = 4
    embeddings = [[float(t) + i * 0.1 for i in range(embed_size)] for t in tokens]
    attention = MiniAttention(embed_size)
    output, weights = attention.forward(embeddings)

    print("Attention Weights:")
    for row in weights:
        print(["%.2f" % w for w in row])
    print("Transformer Math Done!")
