# medical_prescription_extract.py

# Install the required library
%pip install -U -q google-genai

# Import required libraries
from google import genai
client = genai.Client(api_key=GOOGLE_API_KEY)  # Replace with your actual Google API key

import re
import os
import json
from PIL import Image
import pandas as pd
from google.generativeai import GenerativeModel

# Function to clean response text
def clean_response_text(text):
    return text.replace("null", "None")

# Function to extract and clean JSON from response
def extract_json_from_response(text):
    # Remove markdown formatting if present
    text = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.DOTALL)
    
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)

    try:
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Raw cleaned response:\n", text)
        return []

# Define image folder path
image_folder = "/kaggle/input/illegible-medical-prescription-images-dataset/data"
image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(".jpg")])
total_images = len(image_files)
batch_size = 10  # Define how many images to process at a time

# Prompt for the LLM
base_prompt = (
    "You are a medical document extraction assistant. "
    "For each prescription image provided, extract the following data in JSON format: "
    "1. Clinic or hospital name\n"
    "2. Patient name\n"
    "3. Patient age\n"
    "4. Patient gender\n"
    "5. Information on disease or any other details needed to be captured\n" 
    "6. List of medicines with fields: name, dosage, frequency\n"
    "If a field is missing, use null.\n"
    "Just return the number as age of the patient. Don't add anything with it.\n"
    "Enter the gender as M or F only.\n"
    "Return only the JSON array, without any markdown or explanation.\n\n"
    "Format:\n"
    "[\n"
    "  {\n"
    "    \"clinic_name\": str or null,\n"
    "    \"patient_name\": str or null,\n"
    "    \"age\": integer or null,\n"
    "    \"gender\": str or null,\n"
    "    \"other\": str or null,\n"
    "    \"medicines\": [\n"
    "      {\"name\": str or null, \"dosage\": str or null, \"frequency\": str or null},\n"
    "      ...\n"
    "    ]\n"
    "  },\n"
    "  ...\n"
    "]"
)

# List to store all structured data
normalized_results = []

# Process images in batches
for i in range(0, total_images, batch_size):
    batch_files = image_files[i:i+batch_size]
    images = []
    file_indices = []

    # Load each image in the batch
    for file in batch_files:
        try:
            img = Image.open(file).convert("RGB")
            images.append(img)
            idx = int(os.path.basename(file).replace(".jpg", ""))
            file_indices.append(idx)
        except Exception as e:
            print(f"Error loading image {file}: {e}")

    # Prepare the prompt and image content for the API
    contents = [base_prompt] + images
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents
    )
    
    # Extract structured JSON data from model output
    batch_results = extract_json_from_response(response.text)

    # Normalize and structure the extracted data
    for result, index in zip(batch_results, file_indices):
        common_data = {
            "index": index,
            "clinic_name": result.get("clinic_name"),
            "patient_name": result.get("patient_name"),
            "age": result.get("age"),
            "gender": result.get("gender"),
            "other": result.get("other")
        }
        for med in result.get("medicines", []):
            row = {
                **common_data,
                "medicine_name": med.get("name"),
                "dosage": med.get("dosage"),
                "frequency": med.get("frequency")
            }
            normalized_results.append(row)

# Convert results to DataFrame
df = pd.DataFrame(normalized_results)
print(df.head())
