import requests

amount = int(input("enter amt:"))
years = float(input("enter years:"))
url = "http://127.0.0.1:5000/getloandeets"
data = {"amount": amount, "years": years}

response = requests.post(url, json=data)
print(response.json())


url_pdf = "http://127.0.0.1:5000/getLoanDetailsPDF"
data_pdf = {"loanAmount": amount, "tenure": years}

pdf_response = requests.post(url_pdf, json=data_pdf)

if pdf_response.status_code == 200:
    with open("LoanDetails.pdf", "wb") as f:
        f.write(pdf_response.content)
    print("\nPDF file saved as 'LoanDetails.pdf'")
else:
    print("\nFailed to generate PDF:", pdf_response.text)