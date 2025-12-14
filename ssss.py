# web_server.py - يعمل على Pydroid3 بدون مشاكل المنافذ
from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "📱 خادم Android للتحكم عن بعد"

@app.route('/shell/<command>')
def shell(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'code': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/files')
def list_files():
    path = request.args.get('path', '.')
    items = os.listdir(path)
    return jsonify({'files': items})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
