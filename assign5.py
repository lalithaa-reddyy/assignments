from fastapi import FastAPI, Response
from pydantic import BaseModel
from fpdf import FPDF
 
app = FastAPI()
 
class LoanRequest(BaseModel):
    loan_amount: float
    tenure: int
 
def get_interest_rate(amount):
    if amount <= 3000000:
        return 6.5
    elif 3000001 <= amount <= 5000000:
        return 7.5
    elif 5000001 <= amount <= 9000000:
        return 9.0
    else:
        raise ValueError(" amount out of  range")
 
@app.post("/getLoanDetails")
def get_loan_details(req: LoanRequest):
    rate = get_interest_rate(req.loan_amount)
    total_interest = req.loan_amount * (rate / 100) * req.tenure
    total_amount = req.loan_amount + total_interest
    return {
        "loan_amount": req.loan_amount,
        "tenure": req.tenure,
        "rate": rate,
        "total_interest": total_interest,
        "total_amount": total_amount
    }
 
@app.post("/getLoanDetailsPDF")
def get_loan_details_pdf(req: LoanRequest):
    rate = get_interest_rate(req.loan_amount)
    total_interest = req.loan_amount * (rate / 100) * req.tenure
    total_amount = req.loan_amount + total_interest
 
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Home Loan Details", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Loan Amount: {req.loan_amount}", ln=True)
    pdf.cell(200, 10, txt=f"Tenure (years): {req.tenure}", ln=True)
    pdf.cell(200, 10, txt=f"Interest Rate: {rate}%", ln=True)
    pdf.cell(200, 10, txt=f"Total Interest: {total_interest}", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount: {total_amount}", ln=True)
 
    pdf_output = pdf.output(dest='S').encode('latin1')
    return Response(content=pdf_output, media_type="application/pdf")
 
 