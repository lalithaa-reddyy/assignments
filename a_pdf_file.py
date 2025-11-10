from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Employee Salary Report", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", "B", 12)
pdf.cell(40, 10, "EID", 1, 0, "C")
pdf.cell(60, 10, "Name", 1, 0, "C")
pdf.cell(40, 10, "Dept", 1, 0, "C")
pdf.cell(40, 10, "Salary", 1, 1, "C")

pdf.set_font("Arial", "", 12)
employees = [
    ["101", "abc", "IT", "65000"],
    ["102", "bdfg", "HR", "70000"],
    ["103", "jfh", "HR", "60000"],
    ["104", "ldokf", "Social Media", "72000"],
    ["105", "jswr", "Open src", "68000"],
]

for emp in employees:
    pdf.cell(40, 10, emp[0], 1, 0, "C")
    pdf.cell(60, 10, emp[1], 1, 0, "C")
    pdf.cell(40, 10, emp[2], 1, 0, "C")
    pdf.cell(40, 10, emp[3], 1, 1, "C")

pdf.output("input2.pdf")

