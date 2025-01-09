from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from PIL import Image
import pytesseract  # For OCR-based text extraction
from langchain_community.document_loaders import PyPDFLoader  # For PDF text extraction
import google.generativeai as genai  # For using Gemini AI
import re

# Initialize the FastAPI app
app = FastAPI()

# Allow CORS for communication with React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Gemini AI client (replace with your actual API key)
genai.configure(api_key="AIzaSyAPMPD0yjAdvJCb7jy-VWhKysVn8ZqZjtk")  # Replace with actual API key

@app.post("/submit")
async def submit_application(
    name: str = Form(...),  # User's provided name
    fatherName: str = Form(...),  # Father's Full Name
    sscMarks: str = Form(...),  # SSC Marks
    sscSchool: str = Form(...),  # SSC School Name
    caste: str = Form(...),  # Caste
    gender: str = Form(...),  # Gender
    phone: str = Form(...),
    email: str = Form(...),
    annualIncome: str = Form(...),  # Annual Income
    address: str = Form(...),  # Address
    aadhaarNo: str = Form(...),  # Aadhaar Number
    marksMemo: UploadFile = File(...),  # User's marks memo (PDF)
    casteCertificate: UploadFile = File(...),  # Caste Certificate
    incomeCertificate: UploadFile = File(...),  # Income Certificate
    bonafideCertificate: UploadFile = File(...),  # Bonafide Certificate
    aadhaarDocs: UploadFile = File(...),  # Aadhaar Document
):
    # Save the uploaded files
    try:
        marks_memo_location = f"{UPLOAD_DIR}/{marksMemo.filename}"
        caste_certificate_location = f"{UPLOAD_DIR}/{casteCertificate.filename}"
        income_certificate_location = f"{UPLOAD_DIR}/{incomeCertificate.filename}"
        bonafide_certificate_location = f"{UPLOAD_DIR}/{bonafideCertificate.filename}"
        aadhaar_docs_location = f"{UPLOAD_DIR}/{aadhaarDocs.filename}"

        with open(marks_memo_location, "wb") as file:
            file.write(await marksMemo.read())

        with open(caste_certificate_location, "wb") as file:
            file.write(await casteCertificate.read())

        with open(income_certificate_location, "wb") as file:
            file.write(await incomeCertificate.read())

        with open(bonafide_certificate_location, "wb") as file:
            file.write(await bonafideCertificate.read())

        with open(aadhaar_docs_location, "wb") as file:
            file.write(await aadhaarDocs.read())

        # Extract text from Aadhaar document (if PDF)
        aadhaar_loader = PyPDFLoader(aadhaar_docs_location)
        aadhaar_docs = aadhaar_loader.load()
        aadhaar_text = " ".join([doc.page_content for doc in aadhaar_docs])

        # Use PyPDFLoader to extract text from the uploaded marks memo
        marks_memo_loader = PyPDFLoader(marks_memo_location)
        marks_memo_docs = marks_memo_loader.load()
        marks_memo_text = " ".join([doc.page_content for doc in marks_memo_docs])

        # Implement name extraction logic (can use regex, or AI model)
        extracted_name = "Extracted Name From Marks Memo"  # Implement name extraction logic
        extracted_fathers_name = "Extracted Father's Name"  # Implement father's name extraction logic

        # Generate a prompt for Gemini AI to validate all fields
        prompt = f"""
        You are an AI that can extract and validate information from documents.

        The following is the content of the marks memo (PDF file):

        {marks_memo_text}

        You will also receive the content from the user's submitted application form with the following details:

        - User's Name: {name}
        - User's Father's Name: {fatherName}
        - Caste: {caste}
        - Annual Income: {annualIncome}
        - Aadhaar Number: {aadhaarNo}

        Validation rules:
        - For names, consider variations in spelling (e.g., 'Anik' vs 'Anil') as a mismatch.
        - Consider the order of names (e.g., "Anil Katroth" vs "Katroth Anil") as a valid match.
        - Ensure that the caste, SSC marks, income, and Aadhaar number are compared accurately and completely match the values provided in the certificates.

        Your tasks:

        1. Extract the following information from the marks memo document:
        - Full Name
        - Father's Name

        2. Compare the extracted Full Name and Father's Name from the marks memo with the user's entered data. If there is any mismatch, return "Mismatch" along with an explanation of the mismatch (e.g., spelling differences, name order discrepancies).

        3. Compare the following details between the user's entered data and the provided documents and the name in the below mentioned documents should be same as the marks_memo_text:
        - Caste (compare with the caste certificate data)
        - SSC Marks (compare with the marks memo data)
        - Annual Income (compare with the income certificate data)
        - Aadhaar Number (compare with the Aadhaar certificate data)

        4. If all the details (Caste, SSC Marks, Annual Income, and Aadhaar Number) match exactly with the provided certificates, return "Success." If any detail does not match, return "Mismatch" along with an explanation of what does not match.

        Please provide a final summary with either "Success" or "Mismatch" based on your findings.
        """

        # Generate the response using Gemini AI
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Extract the response text
        response_text = response.text  # Access the text field of the response object

        # Check if all fields match and return success or failure
        if "Success" in response_text:
            return {"response_text": "Success: All details match."}
        else:
            return {"response_text": f"Failure: {response_text}"}

    except Exception as e:
        print(e)
        return {"error": str(e)}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
