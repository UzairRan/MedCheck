# streamlit_app/app.py
import streamlit as st
import sqlite3
from datetime import datetime
from pdf_generator import generate_pdf

# App config
st.set_page_config(page_title="💊 MedCheck", layout="centered")

# CSS (same as your Flask app)
st.markdown("""
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 800px; margin: 20px auto; padding: 20px; }
        h1 { color: #d32f2f; }
        textarea { width: 100%; height: 150px; margin: 10px 0; padding: 10px; }
        button { padding: 10px 20px; background: #1976d2; color: white; border: none; cursor: pointer; }
        button:hover { background: #0d47a1; }
        .risk { padding: 10px; margin: 20px 0; font-size: 1.2em; }
        .high { background: #ffcdd2; color: #c62828; }
        .medium { background: #ffe0b2; color: #bf360c; }
        .low { background: #c8e6c9; color: #1b5e20; }
        .interaction { background: white; padding: 10px; margin: 10px 0; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .disclaimer { font-size: 0.9em; color: #555; margin-top: 30px; }
        .error { color: red; }
        .info { color: green; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>💊 MedCheck</h1>", unsafe_allow_html=True)
st.write("Check if your meds, OTCs, or supplements interact")
st.write("Enter all your medications. Get real-time safety warnings.")

# Input
drugs_input = st.text_area(
    "One drug per line:",
    height=150,
    placeholder="e.g.\nsertraline\ntramadol\nibuprofen\nfish oil"
)

# Normalize drug name
def normalize(name):
    return name.strip().lower().replace('.', '').replace('-', '')

# Database connection
def get_db():
    conn = sqlite3.connect('database/interactions.db')
    conn.row_factory = sqlite3.Row  # Enables row['column_name']
    return conn

# Check interactions
if st.button("Check Interactions"):
    drugs = [normalize(d) for d in drugs_input.split("\n") if d.strip()]
    
    if not drugs:
        st.error("Please enter at least one drug.")
    else:
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

        # Show results
        st.success(f"**Risk Level: {risk_level}**")

        if interactions:
            # Only show "Dangerous Combinations Found" for High Risk
            if risk_level == "High":
                st.markdown("### ⚠️ Dangerous Combinations Found")

            for intr in interactions:
                with st.expander(f"🔴 {intr['pair']}"):
                    st.write(f"**Risk**: {intr['description']}")
                    st.write(f"**Onset**: {intr['onset']}")
                    st.write(f"**Advice**: {intr['advice']}")
                    if intr['food_precautions'] and intr['food_precautions'] != 'N/A':
                        st.write(f"**Diet Warning**: {intr['food_precautions']}")

            # Generate PDF (only trigger generation on button click)
            result = {
                "risk_level": risk_level,
                "interactions": interactions,
                "drugs_entered": [d.title() for d in drugs],
                "timestamp": datetime.now().strftime("%B %d, %Y")
            }

            if st.button("Generate PDF Report"):
                try:
                    st.session_state.pdf_data = generate_pdf(result)
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")

            # Always show download button if PDF is ready
            if 'pdf_data' in st.session_state:
                st.download_button(
                    "📥 Download PDF",
                    data=st.session_state.pdf_data,
                    file_name="MedCheck_Report.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("✅ No serious interactions found.")

# Footer
st.markdown("---")
st.write("Disclaimer: MedCheck provides educational information only. Always consult your healthcare provider before making changes.") 