import aiohttp
import os
import google.generativeai as genai
from project_name.text_extraction import extract_text  # Replace with your actual text extraction module


# Configure the API with your key at the start
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable.")
genai.configure(api_key=api_key)

prompt = "blah blah placeholder say whatssup"


# Function to call Gemini API and get content generation
async def call_gemini_api(prompt: str):
    headers = {"Authorization": f"Bearer {api_key}"}
    model = genai.GenerativeModel('gemini-pro')
    payload = {"model": model, "prompt": prompt}

    async with aiohttp.ClientSession() as session:
        async with session.post(api_key, headers=headers, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result['output']
            else:
                response_text = await response.text()
                raise Exception(f"Error from Gemini API: {response.status} - {response_text}")
            

# Function to handle file upload and process content
async def process_uploaded_file(file_data, file_content_type: str):
    # Extract text from the file data
    text_content = await extract_text(file_data, file_content_type)
    
    # Prepend or append any necessary text to the content
    prefix_prompt = "Please summarize the following research paper: "
    full_prompt = prefix_prompt + text_content
    
    # Call Gemini API with the full prompt
    gemini_result = await call_gemini_api(full_prompt)
    
    # Parse the result for numerical data
    numerical_data = parse_gemini_output(gemini_result)
    
    return numerical_data

def parse_gemini_output(self, gemini_text):
    parsed_data = {}
        # Example: parsed_data = {"score": extract_score(gemini_result), "summary": extract_summary(gemini_result)}

    return parsed_data

# - extract_text(file_data, file_content_type)
# - extract_score(gemini_result)
# - extract_summary(gemini_result)