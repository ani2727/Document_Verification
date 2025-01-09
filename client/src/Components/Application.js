import React, { useState } from 'react';
import './Application.css';
import {Link} from 'react-router-dom'

const Application = () => {
    const [formData, setFormData] = useState({
        name: '',
        fatherName: '',
        sscMarks: '',
        sscSchool: '',
        caste: '',
        gender: '',
        phone: '',
        email: '',
        annualIncome: '',
        address: '',
        aadhaarNo: '',
        marksMemo: null,
        casteCertificate: null,
        incomeCertificate: null,
        bonafideCertificate: null,
        aadhaarDocs: null,
    });

    const [response, setResponse] = useState(null); // To store API response
    const [loading, setLoading] = useState(false); // To show a loading state
    const [showSuccessModal, setShowSuccessModal] = useState(false); // Modal visibility state

    // Handle input changes
    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setFormData({
            ...formData,
            [name]: files ? files[0] : value, // Handle single file input
        });
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); // Start loading when the form is submitted

        const data = new FormData();
        for (const key in formData) {
            data.append(key, formData[key]); // Append form data fields
        }

        try {
            // Send POST request to the backend
            const response = await fetch('http://127.0.0.1:8000/submit', {
                method: 'POST',
                body: data,
            });

            // Check if the response is OK
            if (response.ok) {
                const result = await response.json();
                setResponse(result); // Store response data from the backend
                
                // Check the response for success or failure
                if (result.response_text === "Success") {
                    setShowSuccessModal(true); // Show success modal after successful submission
                }
            } else {
                const errorData = await response.json();
                setResponse({
                    response_text: 'Error: Something went wrong!',
                    message: `Server responded with: ${JSON.stringify(errorData)}`,
                    success: false,
                });
            }
        } catch (error) {
            console.error('Error:', error);
            setResponse({
                response_text: 'Error: Something went wrong!',
                message: 'An error occurred while submitting the application.',
                success: false,
            });
        } finally {
            setLoading(false); // End loading state
        }
    };

    // Close the success modal after a few seconds or when the user clicks 'Close'
    const handleCloseModal = () => {
        setShowSuccessModal(false);
    };

    return (
        <div className="application">
            <h2>Online Admission Application Form</h2>
            <form onSubmit={handleSubmit}>
                {/* Personal Information */}
                <div className="form-group">
                    <label htmlFor="name">Full Name:</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="fatherName">Father's Full Name:</label>
                    <input
                        type="text"
                        id="fatherName"
                        name="fatherName"
                        value={formData.fatherName}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="sscMarks">SSC Marks:</label>
                    <input
                        type="number"
                        id="sscMarks"
                        name="sscMarks"
                        value={formData.sscMarks}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="sscSchool">SSC School:</label>
                    <input
                        type="text"
                        id="sscSchool"
                        name="sscSchool"
                        value={formData.sscSchool}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="caste">Caste:</label>
                    <input
                        type="text"
                        id="caste"
                        name="caste"
                        value={formData.caste}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="gender">Gender:</label>
                    <select
                        id="gender"
                        name="gender"
                        value={formData.gender}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="phone">Phone Number:</label>
                    <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="annualIncome">Annual Income:</label>
                    <input
                        type="number"
                        id="annualIncome"
                        name="annualIncome"
                        value={formData.annualIncome}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="address">Address:</label>
                    <textarea
                        id="address"
                        name="address"
                        value={formData.address}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="aadhaarNo">Aadhaar Number:</label>
                    <input
                        type="text"
                        id="aadhaarNo"
                        name="aadhaarNo"
                        value={formData.aadhaarNo}
                        onChange={handleChange}
                        required
                    />
                </div>

                {/* File Uploads - PDF only */}
                <div className="form-group">
                    <label htmlFor="marksMemo">Marks Memo (PDF):</label>
                    <input
                        type="file"
                        id="marksMemo"
                        name="marksMemo"
                        accept=".pdf"
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="casteCertificate">Caste Certificate (PDF):</label>
                    <input
                        type="file"
                        id="casteCertificate"
                        name="casteCertificate"
                        accept=".pdf"
                        onChange={handleChange}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="incomeCertificate">Income Certificate (PDF):</label>
                    <input
                        type="file"
                        id="incomeCertificate"
                        name="incomeCertificate"
                        accept=".pdf"
                        onChange={handleChange}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="bonafideCertificate">Bonafide Certificate (PDF):</label>
                    <input
                        type="file"
                        id="bonafideCertificate"
                        name="bonafideCertificate"
                        accept=".pdf"
                        onChange={handleChange}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="aadhaarDocs">Aadhaar Document (PDF):</label>
                    <input
                        type="file"
                        id="aadhaarDocs"
                        name="aadhaarDocs"
                        accept=".pdf"
                        onChange={handleChange}
                    />
                </div>

                <button type="submit" disabled={loading} className="submit-btn">
                    {loading ? 'Submitting...' : 'Submit Application'}
                </button>
            </form>

            {response && (
                <div className='foot'>
                    <div className={`response ${response.response_text === "Success" ? 'success' : 'error'}`}>
                    <h3>Application Result</h3>
                    <p><strong>Response:</strong> {response.message}</p>
                    
                    </div>
                    <Link to='/'><button>Close</button></Link>
                </div>
            )}

            {/* Success Modal */}
            {showSuccessModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Your application has been submitted successfully!</h3>
                        <button onClick={handleCloseModal}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Application;
