# OmniLLM - 无人能比的极客全栈大模型架构

## 1. 核心底层结构 (Core)
- **Zero-Dependency Tokenizer**: 手写 BPE 分词器，完全不依赖第三方库。
- **Tensor Engine**: 用纯 C / 纯 Python 写底层张量计算（矩阵乘、Softmax、LayerNorm），彻底搞懂大模型怎么算的。
- **Transformer From Scratch**: 不用 PyTorch 的 `nn.Transformer`，从零手写 Attention（多头注意力机制）和位置编码。

## 2. 模型微调与推理 (Model)
- **支持 GGUF**: 接入 llama.cpp 生态。
- **LoRA 训练**: 在 Win7 纯 CPU / 有限显存下进行轻量微调。
- **MCP 协议**: 模型原生支持调用外部工具（Model Context Protocol）。

## 3. 全端发布 (Deploy)
- **Web**: 使用 Node.js + HTML/JS 搭建纯本地网页版。
- **App**: 通过 PWA 或轻量套壳，打包成 Android/Windows 应用。
- **Agent**: 具有记忆、规划、工具调用能力的自主智能体。