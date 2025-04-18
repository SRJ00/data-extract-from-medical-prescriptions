```mermaid
graph TD
    A[Extracted Data - extracted_data.csv] --> B[Group Data by Prescription_ID]
    B --> C[Build Validation Prompt - Prescription Info & Medicines]
    C --> D[Gemini Text Model - Validate Medicines and Dosages]
    D --> E[Validated JSON - validity of drug and dosage, associated reason]
    E --> F[Flag Unsafe Combinations, Dosage Issues]
    F --> G[Merge Validation Results with Extracted Data]
    G --> H[Save Validated Data - validated_prescriptions.csv]
