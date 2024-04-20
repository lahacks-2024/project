import reflex as rx

class FormState(rx.State):

    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data

class UploadState(rx.State):
    "The app state."

    # The images to show.
    img: list[str]

    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        "Handle the upload of file(s)."
        
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)
            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(f"/{file.filename}")

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


rx.vstack(
    rx.upload(
        rx.vstack(
            rx.button(
                "Select File",
            ),
            rx.text(
                "Drag and drop files here or click to select files"
            ),
        ),
        padding="5em",
    ),
    rx.hstack(rx.foreach(rx.selected_files, rx.text)),
    rx.button(
        "Upload",
        on_click=lambda: UploadState.handle_upload(
            rx.upload_files()
        ),
    ),
    rx.button(
        "Clear",
        on_click=rx.clear_selected_files,
    ),
    rx.foreach(
        UploadState.img, lambda img: rx.image(src=img, width="20%", height="auto",)
    ),
    padding="5em",
    width="100%",
)