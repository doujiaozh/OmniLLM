# -*- coding: utf-8 -*-
import http.server
import socketserver
import json
import subprocess
import os

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_text = data.get('text', '')

            print(f"[OmniLLM] 真实大模型正在处理: {user_text}")

            # 调用你本地编译好的 llama.cpp 进行真实推理！
            # 注意：把模型路径换成你本地真实的 gguf 路径
            model_path = r"D:\ZhouYongJie\Download\Qwen3-0.6B-Q4_K_M.gguf"
            exe_path = r"D:\Code\llama-cpp\bin\llama-cli.exe"
            
            try:
                # 构造 llama-cli 命令，限制生成长度以加快速度
                cmd = [
                    exe_path, "-m", model_path, 
                    "-p", f"User: {user_text}\nAI:", 
                    "-n", "128", "-t", "4", "--no-display-prompt"
                ]
                
                # 运行命令并获取输出
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                reply = result.stdout.strip()
                
                # 清理多余的换行和提示词
                if not reply:
                    reply = "模型无输出，可能是内存不足或模型路径错误。"
                    
            except Exception as e:
                reply = f"模型调用失败: {str(e)}"

            response = json.dumps({"reply": reply}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response)

PORT = 8000
with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
    print(f"OmniLLM 真实大模型后端已启动！请访问 http://<你的电脑IP>:{PORT}")
    httpd.serve_forever()