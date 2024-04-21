import reflex as rx
import os 
import io 
from project_name.services import process_uploaded_file
import google.generativeai as genai
from project_name.text_extraction import extract_text


# Configure the API with your key at the start
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable.")
genai.configure(api_key=api_key)

preprompt = os.getenv("PREPROMPT")
if not preprompt:
    raise ValueError("PREPROMPT is not set. Please set the environment variable.")

class FormState(rx.State):

    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data

class UploadState(rx.State):
    "The app state."

    # The images to show.
    img: list[str] = []
    evaluation_result = dict = {}
    processing: bool = False
    error_message: str = ""


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        "Handle the upload of file(s)."
        self.processing = True
        try:
            for file in files: 
                content_type = file.content_type
                file_data = await file.read()
                full_prompt = preprompt + await extract_text(io.BytesIO(file_data), content_type)
                result = await process_uploaded_file(full_prompt)
                self.evaluation_result = result
        except Exception as e:
            self.error_message = str(e)
        finally:
            self.processing = False
        
        

from project_name.template import template

def form_example():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                ),
                rx.hstack(
                    rx.checkbox("Checked", name="check"),
                    rx.switch("Switched", name="switch"),
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.form_data.to_string()),
    )

def forms():
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    background_color="transparent",
                    color="black"
                )
            ),
            rx.text(
                "Drag and drop files here or click to select files",
                class_name="text-center"
            ),
            class_name="flex flex-col justify-center items-center border-black border-2 rounded-lg p-12 w-96 h-48"
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text)),
        rx.box(
            rx.button(
                "Scan",
                on_click=lambda: UploadState.handle_upload(rx.upload_files()),
            ),
            rx.button(
                "Clear",
                on_click=rx.clear_selected_files,
            ),
            class_name="flex flex-row gap-4",
        ),
        
        rx.foreach(
            UploadState.img, lambda img: rx.image(src=img, width="20%", height="auto",)
        ),
        width="100%",
    )