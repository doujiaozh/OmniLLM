# -*- coding: utf-8 -*-
import http.server
import socketserver
import json
import subprocess
import os
import re

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            user_text = data.get('text', '')

            print(f"\n[OmniLLM] 收到指令: {user_text}，底层引擎启动中...")

            exe_path = r"D:\Code\llama-cpp\bin\llama-cli.exe"
            model_path = r"D:\ZhouYongJie\Download\Qwen3-0.6B-Q4_K_M.gguf"
            prompt_file = "temp_prompt.txt"

            # 修改 1：使用最标准的 Qwen 提示词格式，去掉多余干扰
            prompt_text = (
                f"<|im_start|>system\nYou are a helpful assistant.\n<|im_end|>\n"
                f"<|im_start|>user\n{user_text}<|im_end|>\n"
                "<|im_start|>assistant\n"
            )
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt_text)

            # 修改 2：限制生成长度 -n 64，防止它越写越嗨
            cmd = [
                exe_path, "-m", model_path, 
                "-f", prompt_file, 
                "-n", "64", "-t", "4", 
                "--no-display-prompt", "-no-cnv"
            ]

            try:
                process = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=120,
                    creationflags=0x08000000
                )
                
                reply = process.stdout.strip()
                reply = reply.replace("<|im_end|>", "").replace("[end of text]", "").strip()
                
                # 修改 3：正则暴力清洗所有“心理活动”
                reply = re.sub(r'^(好的|嗯|首先|用户|接下来|这是|根据|我需要|我是一个|作为一个).*?(?=[。！？\n]|$)', '', reply, flags=re.MULTILINE)

                # 修改 4：终极去重（如果小模型复读，只保留第一遍）
                sentences = re.split(r'(?<=[。！？!?])', reply)
                clean_sentences = []
                for s in sentences:
                    if s.strip() and s not in clean_sentences:
                        clean_sentences.append(s)
                reply = "".join(clean_sentences)

            except Exception as e:
                reply = f"引擎报错: {str(e)}"

            if not reply:
                reply = "（模型陷入沉思）"

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode('utf-8'))
            print(f"[OmniLLM] 成功推送到前端！")

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

print("OmniLLM 完全体已启动！请访问 http://192.168.1.71:8000")
with ThreadingHTTPServer(("0.0.0.0", 8000), RequestHandler) as httpd:
    httpd.serve_forever()