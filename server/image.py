
# Function to extract text from images using Tesseract OCR
def extract_text_from_image(image_file):
    image = Image.open(image_file.file)
    return pytesseract.image_to_string(image)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to generate a brief story from the extracted PDF data
def generate_story(marks_memo_text, caste_certificate_text, income_certificate_text, bonafide_certificate_text, aadhaar_docs_text):
    # Here, we want to extract meaningful details from each document

    # Extract Full Name and Father's Name from Marks Memo Text
    full_name_match = re.search(r"(?:Full Name|Name):?\s*([A-Za-z\s]+)", marks_memo_text, re.IGNORECASE)
    father_name_match = re.search(r"(?:Father's Name|Father Name):?\s*([A-Za-z\s]+)", marks_memo_text, re.IGNORECASE)
    
    full_name = full_name_match.group(1).strip() if full_name_match else "Unknown"
    father_name = father_name_match.group(1).strip() if father_name_match else "Unknown"

    # Extract Caste Information from Caste Certificate Text
    caste_match = re.search(r"(?:Caste|Category):?\s*([A-Za-z\s]+)", caste_certificate_text, re.IGNORECASE)
    caste = caste_match.group(1).strip() if caste_match else "Unknown"

    # Extract Annual Income from Income Certificate Text
    income_match = re.search(r"(?:Annual Income|Income):?\s*([\d,]+)", income_certificate_text, re.IGNORECASE)
    annual_income = income_match.group(1).strip() if income_match else "Unknown"

    # Extract Bonafide Information (if available)
    bonafide_match = re.search(r"(?:Bonafide|Student Status):?\s*([A-Za-z\s]+)", bonafide_certificate_text, re.IGNORECASE)
    student_status = bonafide_match.group(1).strip() if bonafide_match else "Unknown"

    # Extract Aadhaar Information from Aadhaar Document Text
    aadhaar_match = re.search(r"(?:Aadhaar Number|Aadhaar ID):?\s*(\d{4}\s?\d{4}\s?\d{4})", aadhaar_docs_text)
    aadhaar_number = aadhaar_match.group(1).strip() if aadhaar_match else "Unknown"

    # Create a brief story
    story = (
        f"{full_name} is a student whose father's name is {father_name}. "
        f"The student is registered under the caste category of {caste}. "
        f"Based on the income certificate, the annual income of the family is {annual_income}. "
        f"As per the bonafide certificate, {full_name} is a valid student at the institution. "
        f"The Aadhaar number associated with {full_name} is {aadhaar_number}."
    )

    return story














############ END

@app.post("/submits")
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
    marksMemo: UploadFile = File(...),  # User's marks memo (Image)
    casteCertificate: UploadFile = File(...),  # Caste Certificate (Image)
    incomeCertificate: UploadFile = File(...),  # Income Certificate (Image)
    bonafideCertificate: UploadFile = File(...),  # Bonafide Certificate (Image)
    aadhaarDocs: UploadFile = File(...),  # Aadhaar Document (Image)
):
    try:
        # Save uploaded files to disk
        marks_memo_location = f"{UPLOAD_DIR}/{marksMemo.filename}"
        caste_certificate_location = f"{UPLOAD_DIR}/{casteCertificate.filename}"
        income_certificate_location = f"{UPLOAD_DIR}/{incomeCertificate.filename}"
        bonafide_certificate_location = f"{UPLOAD_DIR}/{bonafideCertificate.filename}"
        aadhaar_docs_location = f"{UPLOAD_DIR}/{aadhaarDocs.filename}"

        # Save files locally
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

        # Extract text from images and PDFs
        marks_memo_text = extract_text_from_image(marksMemo)  # For images
        caste_certificate_text = extract_text_from_image(casteCertificate)
        income_certificate_text = extract_text_from_image(incomeCertificate)
        bonafide_certificate_text = extract_text_from_image(bonafideCertificate)
        aadhaar_docs_text = extract_text_from_image(aadhaarDocs)

        # If the file is a PDF, use PDF extraction instead of OCR
        if marksMemo.filename.endswith('.pdf'):
            marks_memo_text = extract_text_from_pdf(marksMemo)  # For PDFs
        if casteCertificate.filename.endswith('.pdf'):
            caste_certificate_text = extract_text_from_pdf(casteCertificate)
        if incomeCertificate.filename.endswith('.pdf'):
            income_certificate_text = extract_text_from_pdf(incomeCertificate)
        if bonafideCertificate.filename.endswith('.pdf'):
            bonafide_certificate_text = extract_text_from_pdf(bonafideCertificate)
        if aadhaarDocs.filename.endswith('.pdf'):
            aadhaar_docs_text = extract_text_from_pdf(aadhaarDocs)

        # Generate the user story from the extracted data
        story = generate_story(
            marks_memo_text,
            caste_certificate_text,
            income_certificate_text,
            bonafide_certificate_text,
            aadhaar_docs_text
        )
        print(story)
        return {"story": story}

    except Exception as e:
        print(e)
        return {"error": str(e)}


