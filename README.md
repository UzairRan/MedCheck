# 💊 MedCheck  Drug Interaction Checker

A simple, reliable tool to check dangerous drug interactions  built with Flask, Python, and Streamlit, using a verified SQLite database.

No more "No interaction found" for real dangers like sertraline + tramadol. 


# Many APIs miss critical drug interactions

MedCheck fixes that by using a curated, manually verified database of high-risk combinations cross-checked from  medical sources.



# Why Understanding and Working on This Problem

Patients take multiple medications, OTCs, and supplements, often without knowing the dangers.

After searching various tools, the Current tools are complex, doctor and pharmacist-focused.

No simple, patient-friendly way to check  their meds together for real risks.



# What Was Happening?

Patients didn’t know their drug combos could be dangerous. They used apps that only remind them to take pills, not warn them of harm.

Try It Live

Streamlit App: https://medcheck-cqecu2dumgnvkhmjbxzwhp.streamlit.app/ 




# ✅ Features

→ Check interactions between prescriptions, OTCs, and supplements

→ Clear risk levels: High / Medium / Low

→ Real warnings with onset time, advice, and diet precautions



# 🧱 Tech Stack

Backend: Python

Database: SQLite 

Web: Flask(local host testing, Streamlit)

PDF: pdfkit + wkhtmltopdf(tested on local host)

Templates: Jinja2

Deployment: Streamlit Cloud

Programming: Python, HTML 

# 📁 Project Structure

drugcheck/

│   app.py

│   create_db.py

│   pdf_generator.py

│   requirements.txt

│

├───data/

│   └── drug_interactions.csv

├───database/

│   └── interactions.db

├───streamlit_app/

│   ├── app.py
│   ├── create_db.py
│   ├── pdf_generator.py
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html



# 🔄 Development Flow

🔍 Problem Identification  
   ↳ Feasibility Check  
       ↳ Tool Selection  
           ↳ Code & Build  
               ↳ Validate Results  
                   ↳ Deploy Solution  
                       ↳ Communicate Clearly  
                           ↳ Plan Enhancements  
                               ↳ AI/ML Integration




# What Data Do Patients Enter?

✅ Prescription drugs (e.g., sertraline, tramadol)

✅ Over-the-counter (OTC) medicines (e.g., ibuprofen, omeprazole)

✅ Supplements (e.g., fish oil, St. John’s Wort, melatonin)

✅ One per line,  no complex forms



# What Results Do They Get?

➡️ Risk Level: Low / Medium / High

➡️ Dangerous Combinations: e.g., Sertraline + Tramadol → Risk of serotonin syndrome

➡️ Plain-English Explanation: “This can cause confusion, fast heartbeat, or seizures.”

➡️ Actionable Advice: “Avoid this combo — talk to your doctor.”

➡️ Diet Warnings: “Avoid alcohol” or “Avoid grapefruit juice”



# 📚 Data Source
Interactions are manually curated and cross-verified from:

FDA guidelines

DrugBank 

PubMed

Clinical pharmacology

RxNorm

Take help from AI Tools as well



# Future Enhancements for AI and ML 

✔️ AI-powered prediction of unknown interactions

✔️ User profiles & history

✔️ Email report



# Vision

MedCheck is built with patient safety in mind,  combining verified data, intuitive design, and scalable tech to make drug interaction checking simple, accurate, and accessible



