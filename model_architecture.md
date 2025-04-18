```mermaid
graph TD
    A[Handwritten Prescription Images] --> B[Batch Images <br> <10 images per batch>]
    B --> C[Gemini Vision Model-OCR and Data Extraction]
    C --> D[Extracted JSON<br>Patient Info: Name, Age, Gender, Hospital Name]
    D --> E[Extracted Medicines<br>Name, Dosage, Frequency]
    E --> F[Combine Patient Info & Medicines<br>into Structured Format]
    F --> G[Save Extracted Data<br>extracted_data.csv]
