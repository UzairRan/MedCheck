# streamlit_app/pdf_generator.py
from fpdf import FPDF
from datetime import datetime

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MedCheck Report", ln=True, align='C')
    pdf.ln(10)

    # Risk Level
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(220, 50, 50) if data["risk_level"] == "High" else \
        pdf.set_text_color(255, 130, 0) if data["risk_level"] == "Medium" else \
        pdf.set_text_color(0, 120, 0)
    pdf.cell(0, 10, f"Risk Level: {data['risk_level']}", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # Drugs Entered
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Entered: {', '.join(data['drugs_entered'])}", ln=True)
    pdf.cell(0, 10, f"Checked On: {data['timestamp']}", ln=True)
    pdf.ln(10)

    # Interactions
    if data["interactions"]:
        if data["risk_level"] == "High":
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(220, 50, 50)
            pdf.cell(0, 10, "⚠️ Dangerous Combinations Found", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)

        for intr in data["interactions"]:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 8, f"• {intr['pair']}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 6, f"Risk: {intr['description']}")
            pdf.multi_cell(0, 6, f"Onset: {intr['onset']}")
            pdf.multi_cell(0, 6, f"Advice: {intr['advice']}")
            if intr.get('food_precautions') and intr['food_precautions'] != 'N/A':
                pdf.multi_cell(0, 6, f"Diet Warning: {intr['food_precautions']}")
            pdf.ln(5)
    else:
        pdf.cell(0, 10, "✅ No serious interactions found.", ln=True)
        pdf.ln(10)

    # Disclaimer
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, "Disclaimer: MedCheck provides educational information only. "
                         "Always consult your healthcare provider before making changes.")

    # Output as bytes
    return pdf.output(dest='S').encode('latin1')  # Returns bytes 