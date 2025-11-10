from flask import Flask, request, jsonify,send_file
from fpdf import FPDF
import io
app = Flask(__name__)

def interest_rates(amt):
    if amt <= 3000000:
        return 6.5
    elif 3100000 <= amt <= 5000000:
        return 7.5
    elif 5000000 < amt <= 9000000:
        return 9.0
    
def calc_loan(amt, yrs):
    rate = interest_rates(amt)
    total_interest = (amt * rate * yrs) / 100
    total_amt = amt + total_interest
    return total_interest, total_amt

@app.route("/getloandeets", methods=["POST"])
def get_loan_details():
    data = request.get_json()
    amount = data.get("amount")
    years = data.get("years")
    total_interest, total_amt = calc_loan(amount, years)
    return jsonify({
        "total_interest": total_interest,
        "total_amount": total_amt
    })
@app.route("/getLoanDetailsPDF", methods=["POST"])
def get_loan_details_pdf():
    data = request.get_json()
    loan_amount = float(data.get("loanAmount"))
    tenure = int(data.get("tenure"))
    rate = interest_rates(loan_amount)
    total_interest = (loan_amount * rate * tenure) / 100
    total_amt = loan_amount + total_interest

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial")
    pdf.cell(0, 10, "Loan Details Report", align="C")

    pdf.cell(0, 10, f"Loan Amt:Rs {loan_amount:}")
    pdf.cell(0, 10, f"tenure: {tenure} years")
    pdf.cell(0, 10, f"interest: {rate}%")
    pdf.cell(0, 10, f"Interest Payable:Rs {total_interest:}")
    pdf.cell(0, 10, f"Total Amount Payable:Rs {total_amt:}")

    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="LoanDetails.pdf",
        mimetype="application/pdf"
        )
if __name__ == "__main__":
    app.run(debug=True)