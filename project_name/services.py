
import os
import aiohttp
import google.generativeai as genai
from project_name.text_extraction import extract_text 

# Configure the API with your key at the start
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable.")
genai.configure(api_key=api_key)



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
async def process_uploaded_file(file_stream, file_content_type: str):
     # Extract text from the file data
    text_content = await extract_text(file_stream, file_content_type)

    # Prepend or append any necessary text to the content
    #ADD HERE 
    full_prompt = text_content

    # Call Gemini API with the full prompt
    gemini_result = await call_gemini_api(full_prompt)

    # Parse the result for numerical data
    numerical_data = parse_gemini_output(gemini_result)

    return numerical_data

# Function to parse Gemini output for numerical scores
def parse_gemini_output(gemini_text):
    # Extract numbers following the pattern "LABEL - xx/100"
    import re
    scores = re.findall(r"\b(\w+)\s*-\s*(\d+)/100\b", gemini_text)
    # Converts list of tuples into a dictionary
    parsed_scores = {label: int(score) for label, score in scores}
    return parsed_scores
