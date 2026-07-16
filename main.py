from dotenv import load_dotenv
load_dotenv()

import base64
import io
import os
import shutil
import streamlit as st
from PIL import Image 
import pdf2image
from pdf2image.exceptions import PDFInfoNotInstalledError

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel(DEFAULT_GEMINI_MODEL)
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        #Convert PDF to image
        try:
            poppler_path = shutil.which("pdfinfo")
            if poppler_path:
                poppler_path = os.path.dirname(poppler_path)
            elif os.path.isdir(r"C:\Program Files\poppler\Library\bin"):
                poppler_path = r"C:\Program Files\poppler\Library\bin"
            elif os.path.isdir(r"C:\Program Files (x86)\poppler\Library\bin"):
                poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"

            if poppler_path:
                images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
            else:
                images = pdf2image.convert_from_bytes(uploaded_file.read())
        except PDFInfoNotInstalledError as exc:
            raise RuntimeError(
                "Poppler was not found on PATH. Restart VS Code or the Streamlit terminal after updating PATH, "
                "or ensure Poppler is installed in C:\\Program Files\\poppler\\Library\\bin."
            ) from exc

        first_page = images[0]

        #Convert to Bytes

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()     #Enocode to base64

            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No PDF file uploaded. Please upload a PDF file to proceed.")
    

#Streamlit App
st.set_page_config(page_title = "AI Resume Expert")
st.header("ATS Tracking Resume Analyzer")
input_text = st.text_area("Job Description", key = "input")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"], key="file_uploader")

if uploaded_file is not None:
    st.write("PDF uploaded successfully.")

submit1 = st.button("Tell Me About the Resume")
# submit2 = st.button("How can i improvise my skills")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager with Tech experience in the field of Data science, Full Stack Development, Big Data, DevOps and Data Analytics. Your task is to review the provided resume against the provided job description and provide a detailed analysis of the candidate's qualifications, skills, and experience. Highlight the strengths and weaknesses of the resume in relation to the job requirements. Provide specific feedback on how well the candidate's background aligns with the job description, and suggest areas for improvement or additional information that could enhance the resume's effectiveness. 
"""

input_prompt3 = """
You are a skilled ATS(Applicant Tracking System) with expertise in Data science, Full Stack Development, Big Data, DevOps, Data Analytics and deep ATS functionality. Your task is to analyze the provided resume and job description, and calculate a percentage match score that reflects how well the candidate's qualifications, skills, and experience align with the requirements of the job. Consider factors such as relevant work experience, technical skills, educational background, and any other pertinent information. Provide a clear explanation of the match score, highlighting key areas where the candidate meets or exceeds the job requirements, as well as areas where there may be gaps or opportunities for improvement.
"""

if submit1:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response1 = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.write("Resume Analysis:")
            st.write(response1)
        except RuntimeError as err:
            st.error(str(err))
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response3 = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.write("Percentage Match Analysis:")
            st.write(response3)
        except RuntimeError as err:
            st.error(str(err))
    else:
        st.write("Please upload a PDF file to proceed.")    
