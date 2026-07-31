import streamlit as st
import pdfplumber
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_CLIENT_KEY")
)

# Page settings
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("AI Resume Analyzer")
st.write("Upload your resume and get an AI-powered analysis.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file is not None:

    text = ""

    # Extract text from PDF
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # Check empty resume
    if text.strip() == "":
        st.error("No readable text found in the uploaded resume.")

    else:

        st.subheader("Extracted Resume Text")
        st.text_area("Raw Resume Text", text, height=200)

        if st.button("Analyze Your Resume"):

            with st.spinner("Analyzing resume with Gemini AI..."):

                prompt = f"""
You are an expert ATS (Applicant Tracking System) and resume reviewer.

Analyze the following resume and provide:

1. Candidate Name
2. Top Skills (bullet points)
3. Education
4. Experience Summary
5. Strengths
6. Weaknesses
7. ATS Score out of 100
8. Suggestions to improve the resume

Resume:
{text}
"""

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

                st.success("Resume analysis completed!")

                st.subheader("AI Resume Analysis")
                st.markdown(response.text)

                st.download_button(
                    label="Download Analysis",
                    data=response.text,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )