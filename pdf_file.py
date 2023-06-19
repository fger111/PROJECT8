from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from pymongo import MongoClient
from database import get_latest_record
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
from datetime import date
from PyPDF2 import PdfMerger
import subprocess


def download_pdf_report():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['registration']

    document = get_latest_record()

    text_file = document['lastname'] + ".txt"

    def fetch_text():
        try:
            with open(text_file, "r") as file:
                saved_text = file.read()
        except FileNotFoundError:
            # Handle the case when the file is not found
            pass
        return saved_text

    current_date = date.today()

    formatted_date = current_date.strftime("%B %d, %Y")

    # Create a PDF merger object
    pdf_merger = PdfMerger()

    # Define the report content
    report_title = "Colonoscopy Report"
    patient_firstname = document['firstname']
    patient_lastname = document['lastname']
    age = document['age']
    birthday = document['birthday']
    sex = document['sex']
    address = document['address']
    contact_number = document['contact_number']
    marital_status = document['marital_status']

    findings = fetch_text()

    # Create a PDF document
    doc = SimpleDocTemplate("colonoscopy_report.pdf", pagesize=letter)

    logo_path = r"C:\Users\Franco Gian Ramos\PycharmProjects\pythonProject8\logo.jpg"


    logo_width = 100
    logo_height = 100

    logo_image = Image(logo_path, width=logo_width, height=logo_height)

    # Define styles for the report
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    subtitle_style_2 = styles['Heading3']
    content_style = styles['Normal']
    # Create the report content
    content = []
    content.append(Paragraph("New Sinai MDI Hospital", title_style))
    content.append(Spacer(1, 20))
    content.append(logo_image)
    content.append(Spacer(1, 30))
    content.append(Paragraph(report_title, title_style))
    content.append(Spacer(1, 35))

    table_data = [[Paragraph(f"<u>Patient Name</u>:  {patient_lastname}, {patient_firstname}", subtitle_style),
               Paragraph(f"<u>Date</u>: {formatted_date}", subtitle_style)]]
    table = Table(table_data, colWidths=[300, 200])


    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))  # Align content to the top
    content.append(table)
    content.append(Paragraph(f"<u>Age</u>: {age}", subtitle_style_2))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<u>Sex</u>: {sex}", subtitle_style_2))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<u>Date of Birth</u>: {birthday}", subtitle_style_2))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<u>Address</u>: {address}", subtitle_style_2))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<u>Contact Number</u>: {contact_number}", subtitle_style_2))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"<u>Marital Status</u>: {marital_status}", subtitle_style_2))
    content.append(Spacer(1, 20))
    content.append(Paragraph("<u>Findings</u>:", subtitle_style))
    content.append(Spacer(1, 15))
    content.append(Paragraph(findings, content_style))
    content.append(Spacer(1, 12))

    # Create the PDF document with the report content
    doc.build(content)

    # Add the report to the PDF merger
    pdf_merger.append("colonoscopy_report.pdf")
    filename = "colonoscopy_report.pdf"

    subprocess.Popen([filename], shell=True)
    # Add additional PDF files to the merger if needed
    # pdf_merger.append("additional_file.pdf")

    # Save the merged PDF file
    pdf_merger.write("merged_report.pdf")
    pdf_merger.close()
