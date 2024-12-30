from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import pandas as pd
from xml_generator import create_xml_from_excel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        xml_filename = f"generated_{filename.rsplit('.', 1)[0]}.xml"
        xml_path = os.path.join(app.config['UPLOAD_FOLDER'], xml_filename)
        
        # Save the uploaded file
        file.save(excel_path)
        
        try:
            # Generate XML
            create_xml_from_excel(excel_path, xml_path)
            
            # Return the generated XML file
            return send_file(
                xml_path,
                mimetype='application/xml',
                as_attachment=True,
                download_name=xml_filename
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up uploaded files
            try:
                os.remove(excel_path)
                os.remove(xml_path)
            except:
                pass
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
