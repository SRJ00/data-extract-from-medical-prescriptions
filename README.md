# Extraction and Evaluation Pipeline for Handwritten Medical Prescription

## 1. Extraction Pipeline

### Overview:
The extraction pipeline focuses on transforming handwritten medical prescriptions into structured, actionable data. This is done using optical character recognition (OCR) and multimodal machine learning models to extract patient information and prescription details from image files.

### Steps:
1. **Prescription Images (Handwritten)**: 
   - Input is a batch of images of handwritten prescriptions. These images often feature unclear handwriting, smudges, and messy layouts, making the extraction process challenging.

2. **Batching (10 images per batch)**:
   - Images are processed in batches of 10 to optimize performance and ensure that memory and processing power are managed efficiently.
   
3. **Gemini Flash 2 Model (OCR & Data Extraction)**:
   - **Gemini Flash 2** is a multimodal model that combines both visual and text-based analysis. It performs optical character recognition (OCR) on prescription images, extracting both the text and layout information.
   - The model is designed to handle messy handwriting and the presence of irrelevant text, such as doctor’s notes, instructions, or additional marks that are often found on handwritten prescriptions.
   - The extracted text is parsed into two main sections: **Patient Information** (name, age, gender, clinic) and **Medicines** (name, dosage, frequency).

4. **Extracted JSON (Patient Info)**:
   - The extracted patient information is stored in a structured JSON format.
   - Fields include: Clinic Name, Patient Name, Age, Gender, and other relevant details.

5. **Extracted Medicines**:
   - The medicine information is extracted and includes the medicine name, dosage, and frequency. This information is also formatted into JSON. However, prescriptions often contain extra or irrelevant data that must be filtered out.

6. **Combine Patient Info & Medicines**:
   - The patient info and the list of medicines are combined into a single structured format, ensuring the data is clear and organized for further use.

7. **Save Extracted Data**:
   - Finally, all the extracted and combined data is saved into a CSV file for future use. This CSV contains rows with all the extracted information, making it easy to work with in downstream applications.

---

## 2. Description of Your Multimodal Model Usage

### Overview:
The **Gemini Flash 2** model is employed for extracting and evaluating medical prescription data from images. As a multimodal model, it combines both image and text-based processing to enhance the accuracy of data extraction from messy handwritten prescriptions.

### Models Used:
1. **Gemini Flash 2 Model (Multimodal)**:
   - **Gemini Flash 2** is a cutting-edge multimodal model that can process both visual data (images) and textual data simultaneously. It handles optical character recognition (OCR) to extract text from prescription images, but it also takes into account the layout and context in the image.
   - The model is specifically trained to process handwritten text and extract relevant information, even when the handwriting is unclear or the image contains irrelevant annotations or markings (such as doctor’s notes or instructions).
   - The model performs extraction tasks like identifying patient information, recognizing medicine names, dosages, and frequencies, despite the presence of messy or extraneous data.

### Purpose of Multimodal Approach:
- **Handling Messy Data**: Many handwritten prescriptions are not clean and contain irrelevant information. **Gemini Flash 2** helps filter out these extraneous details, ensuring that only relevant data (e.g., medicines, dosages) is retained.
- **Improved Accuracy**: Combining both visual and textual processing enables the model to better understand and extract information, making it more effective for real-world scenarios where handwritten text is often unclear.
- **Comprehensive Validation**: The model doesn't just extract data; it can also validate the extracted information, providing insights into whether the prescriptions are accurate or contain invalid dosages or medicines.

---

## 3. Evaluation Strategy

### Overview:
The evaluation strategy focuses on validating the quality and accuracy of the extracted prescription data, ensuring that the prescriptions are both logically consistent and medically sound. Given the complexity and messiness of the input data, accuracy is a key challenge.

### Steps in Evaluation:

1. **Validation of Medicine Dosage**:
   - After extraction, each prescription is evaluated for proper medicine dosages. If a dosage is missing, it is flagged and evaluated based on available information.
   - The model checks the prescribed dosages against typical ranges to ensure validity, taking into account unclear handwriting that may make dosage details hard to read.

2. **Identification of Invalid Medications**:
   - The model identifies any medications that are either incorrect or potentially harmful based on known drug interactions, dosages, and contraindications.
   - Medications that are invalid are flagged, and the model generates comments on why the medicine or dosage is problematic. This helps ensure that even with messy handwriting, only valid prescriptions are retained.

3. **Drug-Drug Interaction Detection**:
   - The **Gemini Flash 2** model evaluates potential drug-drug interactions in prescriptions. If any known dangerous interactions are present, they are flagged, ensuring the safety of the patient.

4. **Automated Decision Making**:
   - Each prescription is classified as valid or invalid based on the analysis. Valid prescriptions are flagged with reasons, while invalid prescriptions are highlighted with details on the issues, including invalid medications, unsafe combinations, or missing information.

5. **Final Output**:
   - The evaluation output is a structured JSON response containing:
     - Whether the prescription is valid or invalid.
     - A list of valid medications and those deemed invalid.
     - Any interactions detected between drugs.
     - Comments explaining the reasons for the validation or invalidation.

### Accuracy:
- **60% accuracy**: The validation process has shown a **60% accuracy** rate in identifying valid prescriptions, which includes both correct and problematic cases. Given the nature of handwritten prescriptions, this is a promising result. The challenge remains in dealing with unclear handwriting, missing or ambiguous dosages, and the presence of irrelevant data in prescriptions.

### Benefits:
- **Improved Accuracy**: The evaluation system ensures that prescriptions are validated, reducing errors in medical practice.
- **Safety**: By detecting unsafe drug combinations and dosage issues, it helps prevent harmful mistakes in prescription fulfillment.
- **Automation**: The entire process from extraction to evaluation is automated, saving time and resources in medical settings and reducing the chances of human error.

---

This approach enables a comprehensive and efficient system for extracting and evaluating medical prescriptions, ensuring both data quality and patient safety despite the challenges of unclear handwriting and messy prescriptions.
