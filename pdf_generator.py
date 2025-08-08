# pdf_generator.py
import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

def generate_pdf(data, output_path="medcheck_report.pdf"):
    # Load HTML template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('result.html')
    
    # Render HTML with data
    html_out = template.render(**data)

    # Configure pdfkit (Windows path)
    
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe') 

    # Generate PDF
    pdfkit.from_string(html_out, output_path, configuration=config)