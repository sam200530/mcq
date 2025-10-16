import os
import tempfile
from flask import Flask, render_template, request, send_file, jsonify
import pdfplumber
import docx
from werkzeug.utils import secure_filename
from fpdf import FPDF
import google.generativeai as genai

# ================== Flask Setup ==================
app = Flask(__name__, template_folder='../templates')

# Configure for Vercel
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

# ================== Gemini Setup ==================
# Use environment variable for API key
api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyBhtEb1lvrLiuP6OD677R4cOFHu_PYHUHQ'
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ================== File Handling ==================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            return ''.join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif ext == 'docx':
        doc = docx.Document(file_path)
        return ' '.join([para.text for para in doc.paragraphs])
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    return None

# ================== MCQ Generation ==================
def generate_mcqs_with_gemini(text, num_questions):
    prompt = f"""
You are an AI assistant helping the user generate multiple-choice questions (MCQs) from the text below:

Text:
{text}

Generate {num_questions} MCQs. Each should include:
- A clear question
- Four answer options labeled A, B, C, and D
- The correct answer clearly indicated at the end

Format:
## MCQ
Question: [question]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# ================== Save Results ==================
def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)

    # Create temporary file for PDF
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    pdf.output(temp_path)
    return temp_path

# ================== Routes ==================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_mcqs():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Please upload PDF, DOCX, or TXT files."}), 400

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_upload_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(temp_upload_path)

        # Extract text
        text = extract_text_from_file(temp_upload_path)
        if not text:
            return jsonify({"error": "Could not extract text from the file."}), 400

        # Generate MCQs
        num_questions = int(request.form.get('num_questions', 5))
        mcqs = generate_mcqs_with_gemini(text, num_questions)

        # Create PDF
        base_name = filename.rsplit('.', 1)[0]
        pdf_filename = f"generated_mcqs_{base_name}.pdf"
        pdf_path = create_pdf(mcqs, pdf_filename)

        # Return results with download link
        return render_template('results.html', 
                             mcqs=mcqs, 
                             txt_filename=None, 
                             pdf_filename=pdf_filename,
                             pdf_content=mcqs)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    finally:
        # Clean up temporary files
        try:
            if 'temp_upload_path' in locals() and os.path.exists(temp_upload_path):
                os.remove(temp_upload_path)
        except:
            pass

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # For PDF downloads, create the PDF on demand
        if filename.endswith('.pdf'):
            # This would need to be implemented based on your specific needs
            return jsonify({"error": "PDF download not available in this demo"}), 404
        
        # For text downloads, return the content as text
        if filename.endswith('.txt'):
            return jsonify({"error": "Text download not available in this demo"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 500

# ================== Vercel Handler ==================
def handler(request):
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == "__main__":
    app.run(debug=True)
