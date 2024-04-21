import reflex as rx
import os
import io
from project_name.services import process_uploaded_file
from project_name.text_extraction import extract_text

class FormState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data

class UploadState(rx.State):
    img: list[str] = []
    evaluation_result: dict = {}
    processing: bool = False
    error_message: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.processing = True
        self.error_message = ""
        try:
            for file in files:
                content_type = file.content_type
                file_data = await file.read()
                text_content = await extract_text(io.BytesIO(file_data), content_type)
                
                # Assuming preprompt is already defined in your environment
                preprompt = os.getenv("PREPROMPT")
                full_prompt = preprompt + text_content
                
                # Call the Gemini API
                self.evaluation_result = await process_uploaded_file(full_prompt)
                
                # Save the file for viewing
                outfile = rx.get_asset_path(file.filename)
                with open(outfile, "wb") as file_object:
                    file_object.write(file_data)
                self.img.append(f"/assets/{file.filename}")

        except Exception as e:
            self.error_message = str(e)
        finally:
            self.processing = False

from project_name.template import template

def form_example():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(name="first_name", placeholder="First Name"),
                rx.input(name="last_name", placeholder="Last Name"),
                rx.hstack(
                    rx.checkbox(name="check", label="Checked"),
                    rx.switch(name="switch", label="Switched"),
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(lambda: FormState.form_data.to_string()),
    )

def forms():
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button("Select File", background_color="transparent", color="black")
            ),
            rx.text("Drag and drop files here or click to select files", class_name="text-center"),
            class_name="flex flex-col justify-center items-center border-black border-2 rounded-lg p-12 w-96 h-48"
        ),
        rx.hstack(rx.foreach(lambda: rx.selected_files, rx.text)),
        rx.box(
            rx.button("Scan", on_click=lambda: UploadState.handle_upload(rx.upload_files())),
            rx.button("Clear", on_click=rx.clear_selected_files),
            class_name="flex flex-row gap-4",
        ),
        rx.foreach(lambda: UploadState.img, lambda img: rx.image(src=img, width="20%", height="auto")),
        width="100%",
        class_name="flex justify-center items-center",
    )
