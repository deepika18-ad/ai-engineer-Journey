import streamlit as st
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
import os

# -------------------- Load API Key --------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_CLIENT_KEY")
)

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="PDF Summarizer",
    layout="centered"
)

# -------------------- Header --------------------
st.title("PDF Summarizer")

st.markdown(
    "Upload a PDF and let **Gemini AI** generate a concise summary in seconds."
)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("About")
    st.write(
        "This application summarizes PDF documents using Google's Gemini AI."
    )

    st.divider()

    st.subheader("Steps")
    st.write("1. Upload a PDF")
    st.write("2. Click **Summarize**")
    st.write("3. Download the summary")

# -------------------- Upload Section --------------------
with st.container():

    st.subheader("Upload PDF")

    pdf = st.file_uploader("Choose a PDF", type="pdf")

    if st.button("Summarize"):

        if pdf is None:
            st.warning("⚠️ Please upload a PDF file.")

        else:
            try:
                # Read PDF
                reader = PdfReader(pdf)

                text = ""

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

                # Check if PDF contains readable text
                if text.strip() == "":
                    st.error("No readable text found in this PDF.")

                else:
                    # Generate summary
                    with st.spinner("Generating summary..."):

                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=f"""
Summarize the following PDF.

Requirements:
- Use simple language.
- Keep the summary concise.
- Present the summary in bullet points.
- Highlight the key ideas.

{text}
"""
                        )

                    st.success("Summary generated successfully!")

                    st.subheader("Summary")

                    st.write(response.text)

                    st.download_button(
                        label="Download Summary",
                        data=response.text,
                        file_name="summary.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"Something went wrong:\n\n{e}")