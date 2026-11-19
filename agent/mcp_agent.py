# -*- coding: utf-8 -*-
# 模拟一个极简的 Agent 规划器
class OmniAgent:
    def __init__(self):
        self.tools = {
            "search_web": self.search_web,
            "run_code": self.run_code
        }

    def search_web(self, query):
        return f"[工具执行] 搜索了: {query}，返回了 3 条结果。"

    def run_code(self, code):
        return f"[工具执行] 成功运行代码，输出: Hello OmniLLM!"

    def think_and_act(self, user_prompt):
        print(f"用户: {user_prompt}")
        # 这里模拟大模型分析意图，并决定调用工具
        if "搜索" in user_prompt:
            print("OmniLLM 正在思考: 需要调用 search_web")
            result = self.tools["search_web"](user_prompt)
        elif "运行" in user_prompt:
            print("OmniLLM 正在思考: 需要调用 run_code")
            result = self.tools["run_code"](user_prompt)
        else:
            result = "普通回复: 我不需要工具也能回答你。"
        
        print(f"Agent 最终回复: {result}\n")

if __name__ == "__main__":
    agent = OmniAgent()
    agent.think_and_act("帮我搜索一下今天的最新AI新闻")
    agent.think_and_act("帮我运行一段 Python 代码")