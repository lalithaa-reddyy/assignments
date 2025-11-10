from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", "", 12)

text = "Reading and Extracting data from pdf to excel Using class and inheritance assignment 3"
pdf.multi_cell(0, 10, text)
pdf.output("input3.pdf")
print("PDF created successfully!")
