# -*- coding: utf-8 -*-
import http.server
import socketserver
import json
import sys
import os

# 引入我们写好的 Agent
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))
from mcp_agent import OmniAgent

agent = OmniAgent()

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 当访问根目录时，返回网页
        if self.path == '/':
            self.path = 'web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # 接收前端发来的聊天请求
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_text = data.get('text', '')

            # 让 Agent 进行思考和决策
            print(f"收到前端请求: {user_text}")
            
            # 这里为了演示，直接抓取 Agent 的控制台输出，并组装成回复
            # 实际大模型会在这里生成文本
            if "搜索" in user_text or "search" in user_text:
                reply = agent.search_web(user_text)
            elif "运行" in user_text or "run" in user_text:
                reply = agent.run_code(user_text)
            else:
                reply = f"OmniLLM 核心已收到: {user_text}"

            response = json.dumps({"reply": reply}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response)

PORT = 8000
with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
    print(f"OmniLLM 后端服务器已启动！请访问 http://<你的电脑IP>:{PORT}")
    httpd.serve_forever()