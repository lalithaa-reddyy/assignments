from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fpdf import FPDF
import os
import asyncio

app = FastAPI()

@app.post("/export-pdf")
async def export_pdf(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Define file path
    file_path = "output7.pdf"

    # Generate the PDF (run blocking task in a thread-safe way)
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Form Data Export", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Message: {message}")
        pdf.output(file_path)

    await asyncio.to_thread(create_pdf)

    # Confirm the file was created
    if not os.path.exists(file_path):
        return {"error": "Failed to create PDF"}

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="form_export.pdf"
    )
