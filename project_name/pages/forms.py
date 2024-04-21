import reflex as rx

class FormState(rx.State):
    
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data

class UploadState(rx.State):
    "The app state."

    # show_dashboard: bool = False

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
        # State.show_dashboard = True

from project_name.template import template

def url_form():
    return rx.vstack(
        # rx.image(src="COMPANY_LOGO_URL", width="200px"),
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

@template
def forms() -> rx.Component:
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
                on_click=lambda: UploadState.handle_upload(
                    rx.upload_files()
                ),
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
        class_name="flex flex-col !justify-center !items-center"
    )