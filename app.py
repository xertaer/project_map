# app.py
import os
import base64
from flask import Flask, render_template
from markupsafe import Markup
from data import DISCOVERERS

app = Flask(__name__)

def get_base64_map():
    """Читает чистую карту из static и переводит в Base64 для стабильной загрузки"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    map_path = os.path.join(static_dir, 'world_map.jpg')
    if os.path.exists(map_path):
        with open(map_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    return ""

def load_all_points():
    """Автоматически сканирует папку points и объединяет код всех 14 HTML-файлов"""
    points_html = ""
    points_dir = os.path.join(os.path.dirname(__file__), 'points')
    
    if os.path.exists(points_dir):
        # Перебираем все файлы в папке по алфавиту
        for file_name in sorted(os.listdir(points_dir)):
            if file_name.endswith('.html'):
                file_path = os.path.join(points_dir, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    points_html += f.read() + "\n"
    return Markup(points_html)

@app.route('/')
def index():
    map_base64 = get_base64_map()
    all_points_code = load_all_points()
    return render_template('index.html', discoverers=DISCOVERERS, map_image=map_base64, points_code=all_points_code)

@app.route('/discoverers')
def discoverers_list():
    return render_template('discoverers.html', discoverers=DISCOVERERS)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
