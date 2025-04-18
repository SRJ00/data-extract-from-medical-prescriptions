# evaluate_prescription.py

# Install the required library
%pip install -U -q google-genai

# Import necessary libraries
from google import genai
client = genai.Client(api_key=GOOGLE_API_KEY)  # Replace with your actual Google API key

import os
import json
import re
from PIL import Image
import pandas as pd
from google.generativeai import GenerativeModel
from tqdm import tqdm

# Load the extracted prescription data
df = pd.read_csv('extracted_data.csv')

# Rename columns for consistency
df.columns = ['prescription_id', 'clinic_name', 'patient_name', 'age', 'gender', 'other',
              'medicine_name', 'dosage', 'frequency']

# Function to extract JSON from response text
def extract_json_from_response(text):
    # Look for JSON block in triple backticks
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    else:
        return text.strip()  # fallback: try parsing raw text

# Preprocess prescriptions into dictionary format for validation
def preprocess_group(df):
    grouped = {}
    for pid, group in df.groupby('prescription_id'):
        grouped[pid] = [{
            'name': row['medicine_name'],
            'dosage': str(row['dosage']) if pd.notnull(row['dosage']) else 'Missing'
        } for _, row in group.iterrows()]
    return grouped

# Create prompt for LLM with batch of prescriptions
def build_batch_prompt(grouped_data):
    prescriptions_json = json.dumps(grouped_data, indent=2)
    return f"""**Medical Validation Task**
Analyze the following prescriptions. For each prescription, validate the list of medicines and dosages.

Input format:
{{
  "prescription_id": [{{"name": "medicine", "dosage": "value"}}]
}}

Analyze each prescription separately:
- Validate individual medicine dosages
- If dosage is missing, validate only based on medicine. That is, if combinations/individual medicine makes sense then it is valid.
- Flag unsafe combinations
- Consider typical dosage ranges and drug-drug interactions

Return result as JSON:
{{
  "prescription_id": {{
    "valid": boolean,
    "reasons": {{
      "valid_meds": list[str],
      "invalid_meds": list[str],
      "interactions": list[str],
      "comments": str
    }}
  }},
  ...
}}

Data:
{prescriptions_json}
"""

# Validate a batch of prescription IDs with the Gemini model
def validate_batch(prescription_ids):
    try:
        batch_df = df[df['prescription_id'].isin(prescription_ids)]
        grouped = preprocess_group(batch_df)
        prompt = build_batch_prompt(grouped)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        raw_text = response.text
        json_str = extract_json_from_response(raw_text)
        result = json.loads(json_str)

        return result

    except Exception as e:
        print(f"Batch failed: {str(e)}")
        return {}

# Collect unique prescription IDs and process in batches
unique_ids = df['prescription_id'].unique()
results = []

for i in tqdm(range(0, len(unique_ids), 10)):
    batch_ids = unique_ids[i:i+10]
    batch_results = validate_batch(batch_ids)
    
    for pid in batch_ids:
        pres_result = batch_results.get(str(pid), {
            "valid": False,
            "reasons": {
                "valid_meds": [],
                "invalid_meds": [],
                "interactions": ["Validation not returned"],
                "comments": "No result from model"
            }
        })

        results.append({
            'prescription_id': int(pid),
            'is_valid': pres_result['valid'],
            'valid_meds': ', '.join(str(med) for med in pres_result['reasons']['valid_meds'] if med),
            'invalid_meds': ', '.join(str(med) for med in pres_result['reasons']['invalid_meds'] if med),
            'interactions': ' | '.join(str(inter) for inter in pres_result['reasons']['interactions'] if inter),
            'comments': pres_result['reasons']['comments']
        })

# Merge validation results with original data
results_df = pd.DataFrame(results)
final_df = df.merge(results_df, on='prescription_id')

# Save the final validated data to a CSV file
final_df.to_csv('validated_prescriptions.csv', index=False)

# Show sample output
print(final_df[['prescription_id', 'medicine_name', 'dosage', 'is_valid', 'comments']].head())
