# streamlit_app/pdf_generator.py
from jinja2 import Environment, FileSystemLoader
import os
from weasyprint import HTML

def generate_pdf(data):
    # Load template
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('result.html')
    
    # Render HTML
    html_out = template.render(**data)

    # Convert HTML to PDF using WeasyPrint
    pdf_data = HTML(string=html_out).write_pdf()
    return pdf_data 