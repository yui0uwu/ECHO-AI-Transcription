import os
from dotenv import load_dotenv # Add this
from openai import OpenAI
import whisper
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

print("Initializing Echo Intel Core (Whisper Base)...")
model_whisper = whisper.load_model("base")

def init_db():
    conn = sqlite3.connect('echo_vault.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  filename TEXT, transcript TEXT, summary TEXT, 
                  keywords TEXT, priority TEXT, color TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def analyze_with_deepseek(transcript):
    prompt = f"""
    You are a Law Enforcement Intelligence Analyst. Analyze this police dispatch transcript:
    "{transcript}"

    Return a JSON object with exactly these keys:
    "summary": A 2-sentence formal executive summary focusing on the primary threat, suspect actions, and status.
    "entities": A list of key players (e.g., "Ben Tauzewood (Suspect)", "Lila (Victim)", "Red S-350 (Vehicle)").
    "priority": "CRITICAL ALPHA", "PRIORITY BRAVO", or "ROUTINE".
    "color": "danger", "warning", or "success".
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a professional police intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"DeepSeek Error: {e}")
        return {"summary": "AI Analysis Failed.", "entities": ["Error"], "priority": "CRITICAL", "color": "danger"}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('echo_vault.db')
    conn.row_factory = sqlite3.Row
    logs = conn.execute('SELECT * FROM logs ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

@app.route('/get_log/<int:log_id>', methods=['GET'])
def get_log(log_id):
    conn = sqlite3.connect('echo_vault.db')
    conn.row_factory = sqlite3.Row
    log = conn.execute('SELECT * FROM logs WHERE id = ?', (log_id,)).fetchone()
    conn.close()
    res = dict(log)
    res['keywords'] = res['keywords'].split(" | ")
    return jsonify(res)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['audio']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    
    result = model_whisper.transcribe(path)
    transcript = result['text'].strip()
    
    intel = analyze_with_deepseek(transcript)
    timestamp = datetime.now().strftime("%H:%M | %b %d, %Y")

    conn = sqlite3.connect('echo_vault.db')
    conn.execute('INSERT INTO logs (filename, transcript, summary, keywords, priority, color, timestamp) VALUES (?,?,?,?,?,?,?)',
                 (file.filename, transcript, intel['summary'], " | ".join(intel['entities']), intel['priority'], intel['color'], timestamp))
    conn.commit()
    conn.close()

    return jsonify({"transcript": transcript, "summary": intel['summary'], "keywords": intel['entities'], "priority": intel['priority'], "color": intel['color'], "timestamp": timestamp})

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.json
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "OFFICIAL INTELLIGENCE REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"PRIORITY: {data['priority']}", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, f"Summary: {data['summary']}")
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "TRANSCRIPT:", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 5, data['transcript'])
    pdf_path = os.path.join(UPLOAD_FOLDER, "report.pdf")
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)