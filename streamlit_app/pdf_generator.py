# streamlit_app/pdf_generator.py
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

def generate_pdf(data):
    # Load template
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('result.html')
    
    # Render HTML
    html_out = template.render(**data)

    # Configure for Windows (dev) and Streamlit Cloud (prod)
    try:
        # Try Streamlit Cloud path first
        config = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')
    except:
        # Fallback to local Windows path
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Generate PDF in memory
    pdf_data = pdfkit.from_string(html_out, False, configuration=config)
    return pdf_data  