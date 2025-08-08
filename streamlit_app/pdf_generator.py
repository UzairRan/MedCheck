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

    # Use Streamlit Cloud path
    config = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf')

    # Generate PDF in memory (return bytes)
    pdf_data = pdfkit.from_string(html_out, False, configuration=config)
    return pdf_data 