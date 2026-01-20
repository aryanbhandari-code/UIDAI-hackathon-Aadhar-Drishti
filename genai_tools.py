import google.generativeai as genai
from fpdf import FPDF
import streamlit as st
import os

# --- AI CONFIGURATION ---
try:
    # 1. Try fetching from Streamlit Cloud Secrets (Best for Deployment)
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    # 2. Backup: Fetch from Environment Variables (Good for Local/Docker)
    api_key = os.getenv("GEMINI_API_KEY")

# 3. Connection Logic
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest') # Uses the "Free & Fast" model
        has_ai = True
    except Exception as e:
        st.error(f"AI Connection Failed: {e}")
        has_ai = False
else:
    # If no key found, we don't crash, but AI features won't work
    st.warning("API Key missing. Please set GEMINI_API_KEY in .streamlit/secrets.toml")
    has_ai = False



def generate_pdf_notice(district, reason, stats, lang="English"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="GOVERNMENT OF INDIA - UIDAI", ln=1, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Automated Anomaly Detection System", ln=1, align='C')
    pdf.ln(20)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"SHOW CAUSE NOTICE: {district.upper()}", ln=1)
    
    pdf.set_font("Arial", size=11)
    
    # AI Drafting
    if has_ai:
        prompt = f"""
        Draft a formal Show Cause Notice for the District Magistrate of {district}.
        Context: The district has been flagged for {reason}.
        Evidence: {stats}.
        Language: {lang}.
        Tone: Strict, Official, Legal. Keep it under 150 words.
        """
        try:
            body = model.generate_content(prompt).text
        except:
            body = f"Notice: Irregularities detected in {district}. Reason: {reason}. Please explain."
    else:
        body = f"NOTICE: Anomaly detected in {district}.\nReason: {reason}.\nData Evidence: {stats}\nPlease submit an explanation within 7 days."
        
    # Handling Encoding for PDF
    safe_body = body.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_body)
    
    pdf.ln(20)
    pdf.cell(200, 10, txt="Signed,", ln=1)
    pdf.cell(200, 10, txt="Regional Director, UIDAI", ln=1)
    
    return pdf.output(dest='S').encode('latin-1')

def vernacular_chat(query, context, lang):
    if not has_ai: return "AI Engine Not Connected. Please configure API Key."
    
    prompt = f"""
    Act as a UIDAI Policy Expert.
    Context Data:
    {context}
    
    User Query: {query}
    
    Instruction: Answer using the data. Respond in {lang} language.
    """
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error: {e}"