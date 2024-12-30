# XML Generator from Excel

A web application that generates XML files from Excel data, following a specific format for tax reporting forms.

## Features

- Upload Excel files through a web interface
- Convert Excel data to structured XML format
- Maintain specific XML formatting and structure
- Support for tax form code 270.00
- Drag-and-drop file upload
- Automatic XML download

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/xml-nalog-generator.git
cd xml-nalog-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Excel File Format

The Excel file should have the following columns:
- form: The form name (e.g., "form_270_00")
- sheet: The sheet name (e.g., "page_270_00_01")
- field: The field name
- value: The value for that field

## Usage

1. Prepare your Excel file according to the required format
2. Visit the web interface at `http://localhost:5000`
3. Drag and drop your Excel file or click to select it
4. Click "Generate XML"
5. The generated XML file will automatically download

## Project Structure

```
xml-nalog-generator/
├── app.py              # Flask web application
├── xml_generator.py    # Core XML generation logic
├── requirements.txt    # Python dependencies
├── templates/         
│   └── index.html     # Web interface template
└── uploads/           # Temporary storage for uploads
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
