from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from PIL import Image
import pytesseract
from langchain_community.document_loaders import PyPDFLoader
import google.generativeai as genai

# Initialize the FastAPI app
app = FastAPI()

# Allow CORS for communication with React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for file uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Gemini AI client (replace with your actual API key)
genai.configure(api_key="AIzaSyAPMPD0yjAdvJCb7jy-VWhKysVn8ZqZjtk")  # Replace with your actual Gemini API key

# Function to extract text from PDF using PyPDFLoader
def extract_text_from_pdf(pdf_path):
    pdf_loader = PyPDFLoader(pdf_path)
    pdf_docs = pdf_loader.load()
    return " ".join([doc.page_content for doc in pdf_docs])

# Function to summarize the documents using Gemini AI
def summarize_documents(marks_memo_text, caste_certificate_text, income_certificate_text, aadhaar_docs_text):
    prompt = f"""
    You are a highly skilled summarizer and validator. You will be provided with several documents. Your task is to generate a concise summary of the key details found in these documents. 
    - Marks Memo: {marks_memo_text}
    - Caste Certificate: {caste_certificate_text}
    - Income Certificate: {income_certificate_text}
    - Aadhaar Document: {aadhaar_docs_text}

    validation rules:
    - Any spelling mistake lead to a mismatch
    - Swapping in variables like(eg. Anil Katroth vs Katroth Anil) both considered to be a valid match
    - Annual Income(eg. INR 70,000 vs 70000) considered to be a match
    - Aadhaar number(eg. 1234 5678 9012 vs 123456789012) considered to be a valid match
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        if hasattr(response, 'candidates') and response.candidates:
            content_parts = response.candidates[0].content.parts
            summary_text = "\n".join([part.text for part in content_parts])
            return summary_text
        else:
            return "Error: No valid content found in Gemini AI response."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to validate user data against the summarized content
def validate_user_data(user_data, summary_text):
    validation_errors = []
    if user_data["name"] not in summary_text:
        validation_errors.append("Name mismatch")
    if user_data["fatherName"] not in summary_text:
        validation_errors.append("Father's name mismatch")
    if user_data["aadhaarNo"] not in summary_text:
        validation_errors.append("Aadhaar number mismatch")
    if user_data["sscMarks"] not in summary_text:
        validation_errors.append("SSC Marks mismatch")
    if user_data["caste"] not in summary_text:
        validation_errors.append("Caste mismatch")
    if user_data["annualIncome"] not in summary_text:
        validation_errors.append("Annual Income mismatch")
    
    # Add more checks for other fields if needed

    if validation_errors:
        return {"response_text": "Failure", "message": ", ".join(validation_errors)}
    return {"response_text": "Success", "message": "Application validated successfully"}

# Main endpoint for submitting the application
@app.post("/submit")
async def submit_application(
    name: str = Form(...), fatherName: str = Form(...), sscMarks: str = Form(...),
    sscSchool: str = Form(...), caste: str = Form(...), gender: str = Form(...), 
    phone: str = Form(...), email: str = Form(...), annualIncome: str = Form(...),
    address: str = Form(...), aadhaarNo: str = Form(...), marksMemo: UploadFile = File(...),
    casteCertificate: UploadFile = File(...), incomeCertificate: UploadFile = File(...),
    bonafideCertificate: UploadFile = File(...), aadhaarDocs: UploadFile = File(...)
):
    try:
        # Save uploaded files to disk
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

        # Extract text from uploaded PDFs
        marks_memo_text = extract_text_from_pdf(marks_memo_location)
        caste_certificate_text = extract_text_from_pdf(caste_certificate_location)
        income_certificate_text = extract_text_from_pdf(income_certificate_location)
        aadhaar_docs_text = extract_text_from_pdf(aadhaar_docs_location)

        # Summarize the documents using Gemini AI
        summary_text = summarize_documents(
            marks_memo_text, caste_certificate_text, income_certificate_text, aadhaar_docs_text
        )
        print(summary_text)
        # Collect user data for validation
        user_data = {
            "name": name,
            "fatherName": fatherName,
            "sscMarks": sscMarks,
            "sscSchool": sscSchool,
            "caste": caste,
            "gender": gender,
            "phone": phone,
            "email": email,
            "annualIncome": annualIncome,
            "address": address,
            "aadhaarNo": aadhaarNo
        }
        print(annualIncome)
        # Validate the user's data against the summarized document text
        validation_response = validate_user_data(user_data, summary_text)

        return validation_response  # Return success or failure response

    except Exception as e:
        return {"response_text": "Failure", "message": f"Error: {str(e)}"}

# Run the application using `uvicorn` (not required if you're deploying it with a WSGI server)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
