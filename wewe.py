# simple_android_server.py
import socket
import threading
import os
import subprocess
import json
import time

class SimpleAndroidServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = True
    
    def start(self):
        """بدء الخادم المبسط"""
        try:
            self.server.bind(('0.0.0.0', self.port))
            self.server.listen(5)
            
            print(f"\n📱 خادم Android المبسط")
            print(f"📍 يعمل على المنفذ: {self.port}")
            print(f"📶 عنوان IP: {self.get_ip()}")
            print("\n⚡ جاهز للاتصال...")
            print("="*50)
            
            while self.running:
                client, addr = self.server.accept()
                print(f"[+] متصل من: {addr[0]}")
                
                client_thread = threading.Thread(target=self.handle_client, args=(client, addr))
                client_thread.start()
                self.clients.append(client)
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
    
    def get_ip(self):
        """الحصول على IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def handle_client(self, client, addr):
        """التعامل مع العميل"""
        try:
            while True:
                # استقبال الأمر
                data = client.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                print(f"[CMD] {addr[0]}: {data}")
                
                # تنفيذ الأمر
                try:
                    result = subprocess.run(data, shell=True, capture_output=True, text=True, timeout=10)
                    
                    response = {
                        'output': result.stdout,
                        'error': result.stderr,
                        'code': result.returncode
                    }
                    
                except subprocess.TimeoutExpired:
                    response = {'error': 'انتهت المهلة'}
                except Exception as e:
                    response = {'error': str(e)}
                
                # إرسال الرد
                client.send(json.dumps(response).encode('utf-8'))
                
        except:
            pass
        finally:
            print(f"[-] انقطع: {addr[0]}")
            client.close()
            if client in self.clients:
                self.clients.remove(client)

# تشغيل الخادم
if __name__ == '__main__':
    server = SimpleAndroidServer(port=9999)
    server.start()
