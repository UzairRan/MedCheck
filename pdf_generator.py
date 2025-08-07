# pdf_generator.py
import pdfkit
from jinja2 import Environment, FileSystemLoader

def generate_pdf(data, output_path="medcheck_report.pdf"):
    # Load template (now self-contained with inline CSS)
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('result.html')
    html_out = template.render(**data)

    # Point to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf='/app/bin/wkhtmltopdf') 

    # Generate PDF
    pdfkit.from_string(html_out, output_path, configuration=config)
    return output_path 