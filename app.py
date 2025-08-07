# app.py
from flask import Flask, request, render_template, flash, session, send_file, redirect
import sqlite3
from datetime import datetime
from pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = "medcheck_secret"  # Required for session

DATABASE = 'database/interactions.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def normalize(name):
    return name.strip().lower().replace('.', '').replace('-', ' ')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        drugs_input = request.form["drugs"]
        drugs = [normalize(d) for d in drugs_input.split("\n") if d.strip()]
        
        if not drugs:
            flash("Please enter at least one medication.")
            return render_template("index.html")

        interactions = []
        seen_pairs = set()

        # Check all 2-drug pairs
        for i, d1 in enumerate(drugs):
            for j, d2 in enumerate(drugs):
                if i >= j:
                    continue
                pair = tuple(sorted([d1, d2]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                conn = get_db()
                c = conn.cursor()
                c.execute('''
                    SELECT * FROM interactions
                    WHERE (LOWER(drug1) = ? AND LOWER(drug2) = ?)
                    OR (LOWER(drug1) = ? AND LOWER(drug2) = ?)
                ''', (d1, d2, d2, d1))
                row = c.fetchone()
                if row:
                    interactions.append({
                        "pair": f"{row['drug1']} + {row['drug2']}",
                        "severity": row["severity"],
                        "description": row["description"],
                        "advice": row["advice"],
                        "onset": row["onset"],
                        "food_precautions": row["food_precautions"]
                    })

        # Risk Level
        high = len([i for i in interactions if i["severity"] == "High"])
        risk_level = "High" if high > 0 else "Medium" if interactions else "Low"

        # Save result in session for PDF generation
        result = {
            "risk_level": risk_level,
            "interactions": interactions,
            "drugs_entered": [d.title() for d in drugs],
            "timestamp": datetime.now().strftime("%B %d, %Y")
        }
        session['pdf_data'] = result  # Save to session

        return render_template("result.html", **result)

    return render_template("index.html")


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf_route():
    # Get data from session
    if 'pdf_data' not in session:
        flash("No data available to generate PDF.")
        return redirect("/")

    result = session['pdf_data']
    pdf_path = "medcheck_report.pdf"

    try:
        # Generate PDF
        generate_pdf(result, output_path=pdf_path)
        # Send file to user
        return send_file(pdf_path, as_attachment=True, download_name="MedCheck_Report.pdf", mimetype='application/pdf')
    except Exception as e:
        flash(f"PDF generation failed: {str(e)}")
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True) 