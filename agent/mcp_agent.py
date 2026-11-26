# -*- coding: utf-8 -*-
class OmniAgent:
    def search_web(self, query):
        return f"[Tool] Searched: {query}, returned 3 results."

    def run_code(self, code):
        return f"[Tool] Executed code, output: Hello OmniLLM!"

    def think_and_act(self, user_prompt):
        print(f"User: {user_prompt}")
        if "search" in user_prompt:
            print("OmniLLM thinking: calling search_web")
            result = self.search_web(user_prompt)
        elif "run" in user_prompt:
            print("OmniLLM thinking: calling run_code")
            result = self.run_code(user_prompt)
        else:
            result = "Normal response."
        print(f"Agent Reply: {result}\n")


if __name__ == "__main__":
    agent = OmniAgent()
    agent.think_and_act("search latest AI news")
    agent.think_and_act("run python code")
