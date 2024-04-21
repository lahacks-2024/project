import os
import io
import reflex as rx
from project_name.text_extraction import extract_text
from project_name.services import process_uploaded_file

class UploadState(rx.State):
    evaluation_result: dict = {}
    processing: bool = False
    error_message: str = ""

    async def handle_local_pdf(self):
        self.processing = True
        try:
            file_path = 'assets/file1.pdf'
            content_type = 'application/pdf'
            # Open the local file
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Extract text from the PDF
            text_content = await extract_text(io.BytesIO(file_data), content_type)

            # Use a predefined prompt from environment variables
            preprompt = os.getenv("PREPROMPT")
            full_prompt = preprompt + text_content

            # Call the Gemini API with the extracted text
            self.evaluation_result = await process_uploaded_file(full_prompt)

        except Exception as e:
            self.error_message = str(e)
        finally:
            self.processing = False
