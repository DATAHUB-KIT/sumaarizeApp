#pip install streamlit google-genai pypdf python-dotenv
import streamlit as st
from google import genai
from pypdf import PdfReader
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Gemini client
client = genai.Client(api_key=api_key)

# Streamlit UI
st.title(" Document Summarizer using Gemini")

st.write("Upload a PDF or TXT document and Gemini will summarize it.")

uploaded_file = st.file_uploader(
    "Upload your document",
    type=["pdf", "txt"]
)

if uploaded_file is not None:

    # Extract text
    if uploaded_file.name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

    else:
        text = uploaded_file.read().decode("utf-8")

    # Display extracted text
    st.subheader("Extracted Document Text")

    st.text_area(
        "Document",
        text,
        height=250
    )

    # Summarize button
    if st.button("Summarize Document"):

        prompt = f"""
        Summarize the following document.

        Provide:
        1. Short summary
        2. Key points
        3. Important facts
        4. Main conclusion

        Document:
        {text}
        """

        with st.spinner("Gemini is summarizing..."):

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        st.subheader(" Gemini Summary")

        st.write(response.text)