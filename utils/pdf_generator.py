from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
def generate_pdf(
    patient_name,
    age,
    gender,
    report_type,
    analysis,
    summary,
    filename="data/output_reports/Medical_Report.pdf"
):
    # -------------------------------------------------
    # PDF Document
    # -------------------------------------------------

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]
    
    # -------------------------------------------------
    # Project Title
    # -------------------------------------------------

    story.append(
        Paragraph(
            "🏥 Medical Report AI Assistant",
            title_style
        )
    )

    story.append(Spacer(1, 0.30 * inch))
    # -------------------------------------------------
    # Patient Information
    # -------------------------------------------------

    story.append(
        Paragraph(
            "Patient Information",
            heading_style
        )
    )

    patient_data = [

        ["Patient Name", patient_name],

        ["Age", str(age)],

        ["Gender", gender],

        ["Report Type", report_type]

    ]

    patient_table = Table(
        patient_data,
        colWidths=[2.2 * inch, 3.8 * inch]
    )

    patient_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(patient_table)

    story.append(Spacer(1, 0.25 * inch))
    # -------------------------------------------------
    # Health Score
    # -------------------------------------------------

    total_parameters = len(analysis)

    abnormal_parameters = sum(
        1
        for details in analysis.values()
        if details["status"] != "Normal"
    )

    if total_parameters > 0:
        health_score = int(
            ((total_parameters - abnormal_parameters) / total_parameters) * 100
        )
    else:
        health_score = 100

    story.append(
        Paragraph(
            "<b>Health Score</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<font color='green' size='14'><b>{health_score}/100</b></font>",
            normal_style
        )
    )

    story.append(Spacer(1, 0.25 * inch))
    # -------------------------------------------------
    # Health Analysis
    # -------------------------------------------------

    story.append(
        Paragraph(
            "Health Analysis",
            heading_style
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    table_data = [
        ["Parameter", "Value", "Unit", "Status"]
    ]

    for parameter, details in analysis.items():

        table_data.append([
            parameter,
            str(details["value"]),
            details["unit"],
            details["status"]
        ])

    analysis_table = Table(
        table_data,
        colWidths=[
            2.0 * inch,
            1.0 * inch,
            1.2 * inch,
            1.2 * inch
        ]
    )

    analysis_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,0), 8),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige)

        ])

    )

    story.append(analysis_table)

    story.append(Spacer(1, 0.25 * inch))
    # -------------------------------------------------
    # AI Summary
    # -------------------------------------------------

    story.append(
        Paragraph(
            "AI Medical Summary",
            heading_style
        )
    )

    story.append(Spacer(1, 0.10 * inch))

    summary = summary.replace("\n", "<br/>")

    story.append(
        Paragraph(
            summary,
            normal_style
        )
    )

    story.append(Spacer(1, 0.25 * inch))  
    # -------------------------------------------------
    # Report Generated
    # -------------------------------------------------

    generated_time = datetime.now().strftime(
        "%d %B %Y | %I:%M %p"
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {generated_time}",
            normal_style
        )
    )

    story.append(Spacer(1, 0.15 * inch))  
    # -------------------------------------------------
    # Disclaimer
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Disclaimer</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            """
    This report has been generated using Artificial Intelligence.

    The analysis is intended only for educational purposes.

    Please consult a qualified healthcare professional before making any medical decisions.
            """,
            normal_style
        )
    )

    story.append(Spacer(1, 0.20 * inch))
    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<font size='9' color='grey'>Generated by Medical Report AI Assistant | Powered by Gemini AI</font>",
            styles["Italic"]
        )
    )
    # -------------------------------------------------
    # Build PDF
    # -------------------------------------------------

    doc.build(story)

    return filename