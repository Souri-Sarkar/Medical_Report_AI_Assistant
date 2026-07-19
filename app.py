import os
import glob
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.pdf_reader import extract_text_from_pdf
from utils.image_reader import load_image
from utils.ocr import extract_text_from_image
from utils.text_cleaner import clean_text

from utils.extractor import MedicalExtractor
from utils.analyzer import MedicalAnalyzer
from utils.ai_summary import generate_summary
from utils.chatbot import ask_medical_ai
from utils.pdf_generator import generate_pdf
from utils.compare_reports import compare_reports

st.set_page_config(
    page_title="Medical Report AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Medical Report AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# Initialize Session State
# ==========================================================

default_state = {
    "report_text": "",
    "medical_values": {},
    "analysis": {},
    "summary": "",
    "messages": []
}

for key, value in default_state.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("🏥 Medical AI Assistant")

    st.markdown("---")

    st.subheader("About")

    st.write(
        """
Upload blood reports, CBC reports, diabetes reports,
liver function reports, kidney reports and receive:

✅ OCR Text Extraction

✅ Medical Parameter Extraction

✅ Health Analysis

✅ AI Medical Summary

✅ AI Chat Assistant

✅ PDF Report
"""
    )

    # -----------------------------------------
    # Developer Information
    # -----------------------------------------

    st.markdown("---")

    st.markdown(
        """
### 👨‍💻 Developer

**Souri Sarkar**

B.Tech CSE

Python • AI • Data Science
"""
    )

    st.markdown("---")

    st.success("Version 2.0")
    # ======================================================
    # Report History
    # ======================================================

    st.markdown("---")

    st.subheader("📂 Report History")

    import glob

    history_files = sorted(
        glob.glob("data/history/*.json"),
        reverse=True
    )

    if history_files:

        for file in history_files:

            st.write("📄", os.path.basename(file))

    else:

        st.info("No previous reports found.")

# ==========================================================
# Main Title
# ==========================================================

st.markdown(
    """
# 🏥 Medical Report AI Assistant

### AI-Powered Healthcare Report Analysis using OCR, NLP & Gemini AI
"""
)


st.divider()
# ==========================================================
# Upload Medical Report
# ==========================================================

st.subheader("📄 Upload Medical Report")

uploaded_file = st.file_uploader(
    "Choose a PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

st.divider()

# ==========================================================
# Patient Information
# ==========================================================

st.subheader("👤 Patient Information")

col1, col2 = st.columns(2)

with col1:

    patient_name = st.text_input(
        "Patient Name"
    )

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=25
    )

with col2:

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )

    report_type = st.selectbox(
        "Report Type",
        [
            "CBC",
            "Blood Test",
            "Diabetes",
            "Liver Function",
            "Kidney Function",
            "Lipid Profile",
            "Other"
        ]
    )

st.divider()

# ==========================================================
# Report Preview
# ==========================================================

st.subheader("📑 Uploaded Report")

if uploaded_file:

    if uploaded_file.type.startswith("image"):

        st.image(
            uploaded_file,
            width=500
        )

    else:

        st.success("PDF uploaded successfully.")

else:

    st.info("Please upload a medical report.")

st.divider()

# ==========================================================
# Analyze Button
# ==========================================================

analyze = st.button(
    "🔍 Analyze Report",
    use_container_width=True
)

# ==========================================================
# Analyze Report
# ==========================================================

if analyze:

    if uploaded_file is None:

        st.error("Please upload a medical report first.")

    else:

        with st.spinner(
            "🤖 Gemini AI is generating insights..."
        ):

            # -----------------------------------------
            # Extract OCR Text
            # -----------------------------------------

            if uploaded_file.type == "application/pdf":

                text = extract_text_from_pdf(uploaded_file)

            else:

                image = load_image(uploaded_file)

                text = extract_text_from_image(image)

            # -----------------------------------------
            # Clean OCR Text
            # -----------------------------------------

            text = clean_text(text)

            # -----------------------------------------
            # Extract Medical Parameters
            # -----------------------------------------

            extractor = MedicalExtractor()

            medical_values = extractor.extract(text)

            # -----------------------------------------
            # Analyze Parameters
            # -----------------------------------------

            analyzer = MedicalAnalyzer()

            analysis = analyzer.analyze(medical_values)

            # -----------------------------------------
            # Generate AI Summary
            # -----------------------------------------

            summary = generate_summary(
                patient_name=patient_name,
                report_type=report_type,
                analysis=analysis
            )

            # -----------------------------------------
            # Save Everything in Session State
            # -----------------------------------------

            st.session_state["report_text"] = text
            st.session_state["medical_values"] = medical_values
            st.session_state["analysis"] = analysis
            st.session_state["summary"] = summary

            st.success("✅ Report analyzed successfully!")
            from datetime import datetime

            history = {
                "patient_name": patient_name,
                "age": age,
                "gender": gender,
                "report_type": report_type,
                "analysis": analysis,
                "summary": summary,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"

            with open(
                f"data/history/{filename}",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    history,
                    file,
                    indent=4
                )
            # ==========================================================
            # Display Results
            # ==========================================================
# ==========================================================
# Display Results
# ==========================================================

if st.session_state["analysis"]:

    text = st.session_state["report_text"]
    medical_values = st.session_state["medical_values"]
    analysis = st.session_state["analysis"]
    summary = st.session_state["summary"]

    # ======================================================
    # Dashboard Statistics
    # ======================================================

    total_parameters = len(analysis)

    abnormal_parameters = sum(
        1
        for details in analysis.values()
        if details["status"] != "Normal"
    )

    normal_parameters = total_parameters - abnormal_parameters

    health_score = max(
        0,
        100 - abnormal_parameters * 8
    )

    # ======================================================
    # Save Files
    # ======================================================

    os.makedirs(
        "data/output_reports",
        exist_ok=True
    )

    with open(
        "data/output_reports/extracted_parameters.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            medical_values,
            file,
            indent=4
        )

    os.makedirs(
        "data/extracted_text",
        exist_ok=True
    )

    with open(
        "data/extracted_text/report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    # ======================================================
    # Tabs
    # ======================================================
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            [
                "📄 Overview",
                "🧪 Parameters",
                "📊 Dashboard",
                "🤖 AI Summary",
                "💬 AI Chat",
                "📥 Download",
                "📈 Compare Reports"
            ]
        )

    # ==========================================================
    # TAB 1 - Overview
    # ==========================================================

    with tab1:

        st.subheader("📄 Medical Report Overview")

        # ------------------------------------------------------
        # Patient Summary
        # ------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Patient",
                patient_name if patient_name else "N/A"
            )

        with col2:

            st.metric(
                "Age",
                age
            )

        with col3:

            st.metric(
                "Gender",
                gender
            )

        with col4:

            st.metric(
                "Report Type",
                report_type
            )

        st.divider()

        # ------------------------------------------------------
        # OCR Extracted Text
        # ------------------------------------------------------

        st.subheader("📄 OCR Extracted Report")

        st.text_area(
            "Extracted Text",
            text,
            height=450
        )

        st.divider()

        # ------------------------------------------------------
        # Quick Summary
        # ------------------------------------------------------

        st.subheader("📌 Quick Report Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Parameters Found",
                len(medical_values)
            )

        with col2:

            st.metric(
                "Normal Parameters",
                normal_parameters
            )

        with col3:

            st.metric(
                "Abnormal Parameters",
                abnormal_parameters
            )

    # ==========================================================
    # TAB 2 - Extracted Parameters
    # ==========================================================

    with tab2:

        st.subheader("🧪 Extracted Medical Parameters")

        if medical_values:

            table = []

            for parameter, details in analysis.items():

                table.append(
                    {
                        "Parameter": parameter,
                        "Value": details["value"],
                        "Unit": details["unit"],
                        "Normal Range": details["normal_range"],
                        "Status": details["status"]
                    }
                )

            df = pd.DataFrame(table)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning("No medical parameters detected.")

    # ==========================================================
    # TAB 3 - Health Dashboard
    # ==========================================================

    with tab3:

        st.subheader("📊 Health Dashboard")

        # ------------------------------------------------------
        # Dashboard Metrics
        # ------------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🏥 Health Score",
                f"{health_score}/100"
            )

        with col2:

            st.metric(
                "✅ Normal Parameters",
                normal_parameters
            )

        with col3:

            st.metric(
                "⚠️ Abnormal Parameters",
                abnormal_parameters
            )

        st.divider()
        

        

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=health_score,
                title={"text": "Health Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"thickness": 0.35},
                    "steps": [
                        {"range": [0, 40], "color": "#ff6b6b"},
                        {"range": [40, 70], "color": "#ffd166"},
                        {"range": [70, 100], "color": "#95d5b2"}
                    ]
                }
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )
        st.divider()

        st.subheader("🥧 Health Status Distribution")

        status_count = {}

        for details in analysis.values():

            status = details["status"]

            status_count[status] = status_count.get(status, 0) + 1

        status_df = pd.DataFrame(
            {
                "Status": list(status_count.keys()),
                "Count": list(status_count.values())
            }
        )

        fig = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.45,
            title="Normal vs High vs Low Parameters"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.divider()

        st.subheader("📊 Medical Parameter Values")

        parameter_data = []

        for parameter, details in analysis.items():

            parameter_data.append(
                {
                    "Parameter": parameter,
                    "Value": details["value"]
                }
            )

        parameter_df = pd.DataFrame(parameter_data)

        fig = px.bar(
            parameter_df,
            x="Parameter",
            y="Value",
            text="Value",
            title="Extracted Medical Parameters"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Medical Parameter",
            yaxis_title="Measured Value",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.divider()

        st.subheader("🩺 Health Parameter Cards")

        cols = st.columns(2)

        for index, (parameter, details) in enumerate(analysis.items()):

            with cols[index % 2]:

                status = details["status"]

                if status == "Normal":
                    icon = "🟢"

                elif status == "High":
                    icon = "🔴"

                else:
                    icon = "🟡"

                with st.container(border=True):

                    st.markdown(f"### {parameter}")

                    st.metric(
                        label="Current Value",
                        value=f"{details['value']} {details['unit']}"
                    )

                    st.markdown(
                        f"**Status:** {icon} **{status}**"
                    )

                    st.caption(
                        f"Normal Range: {details['normal_range']}"
                    )
        # ------------------------------------------------------
        # Health Analysis
        # ------------------------------------------------------

        st.subheader("🩺 Detailed Health Analysis")

        if analysis:

            for parameter, details in analysis.items():

                value = details["value"]
                unit = details["unit"]
                status = details["status"]
                normal_range = details["normal_range"]

                message = (
                    f"**{parameter}**\n\n"
                    f"Value: **{value} {unit}**\n\n"
                    f"Normal Range: **{normal_range}**"
                )

                if status == "Normal":

                    st.success(
                        f"✅ {message}\n\nStatus: **Normal**"
                    )

                elif status == "High":

                    st.error(
                        f"🔴 {message}\n\nStatus: **High**"
                    )

                elif status == "Low":

                    st.warning(
                        f"🟡 {message}\n\nStatus: **Low**"
                    )

                else:

                    st.info(
                        f"ℹ️ {message}\n\nStatus: **{status}**"
                    )

        else:

            st.warning("No analysis available.")

    # ==========================================================
    # TAB 4 - AI Medical Summary
    # ==========================================================

    with tab4:

        st.subheader("🤖 AI Medical Summary")

        if st.session_state["summary"]:

            st.success("AI Summary Generated Successfully")

            with st.container(border=True):

                st.markdown(
                    st.session_state["summary"]
                )
        else:

            st.warning(
                "AI summary is not available."
            )

        st.divider()

        st.info(
            """
⚠️ **Disclaimer**

This AI-generated summary is for educational purposes only.

It should not be considered a medical diagnosis or a substitute
for professional medical advice.
"""
        )
        
    # ==========================================================
    # TAB 5 - AI Medical Chat
    # ==========================================================

    with tab5:

        st.subheader("💬 AI Medical Chat")

        st.info(
                "Ask questions about your uploaded medical report."
            )

        # ------------------------------------------------------
        # Check if a report has been analyzed
        # ------------------------------------------------------

        if not st.session_state["analysis"]:

            st.warning(
                "⚠ Please upload and analyze a medical report first."
            )

        else:

            report_text = st.session_state["report_text"]
            analysis = st.session_state["analysis"]

            # ------------------------------------------------------
            # Initialize Chat History
            # ------------------------------------------------------

            if "messages" not in st.session_state:

                st.session_state["messages"] = []

            # ------------------------------------------------------
            # Display Chat History
            # ------------------------------------------------------

            for message in st.session_state["messages"]:

                with st.chat_message(message["role"]):

                    st.markdown(message["content"])

            # ------------------------------------------------------
            # Chat Input
            # ------------------------------------------------------

            question = st.chat_input(
                "Ask something about your report..."
            )

            if question:

                
                # Save user message
                st.session_state["messages"].append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                with st.chat_message("user"):

                    st.markdown(question)

                # --------------------------------------------------
                # AI Response
                # --------------------------------------------------

                with st.chat_message("assistant"):

                    with st.spinner("Thinking..."):

                        answer = ask_medical_ai(
                            question=question,
                            report_text=report_text,
                            analysis=analysis
                        )

                        # ------------------------------------------
                        # Remove accidental duplicate "Answer" section
                        # ------------------------------------------

                        parts = answer.split("## Answer")

                        if len(parts) > 2:

                            answer = "## Answer" + parts[1]

                        st.markdown(answer)
                # --------------------------------------------------
                # Save AI Response
                # --------------------------------------------------

                st.session_state["messages"].append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            # ------------------------------------------------------
            # Clear Chat Button
            # ------------------------------------------------------

            st.divider()

            if st.button(
                "🗑 Clear Chat",
                use_container_width=True
            ):

                st.session_state["messages"] = []

                st.rerun() 
    # ==========================================================
    # TAB 6 - Download Report
    # ==========================================================

    with tab6:

        st.subheader("📥 Download Medical Report")

        st.write(
            """
Generate a professional PDF report containing:

- Patient Information
- Health Analysis
- AI Medical Summary
- Disclaimer
"""
        )

        st.divider()

        if st.button(
            "📄 Generate PDF Report",
            use_container_width=True
        ):

            with st.spinner("Generating PDF Report..."):

                try:

                    pdf_file = generate_pdf(
                        patient_name=patient_name,
                        age=age,
                        gender=gender,
                        report_type=report_type,
                        analysis=st.session_state["analysis"],
                        summary=st.session_state["summary"]
                    )

                    st.success(
                        "✅ PDF Report Generated Successfully!"
                    )

                    with open(pdf_file, "rb") as file:

                        st.download_button(
                            label="⬇ Download Medical Report",
                            data=file,
                            file_name="Medical_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                except Exception as e:

                    st.error(
                        "❌ Unable to generate PDF."
                    )

                    st.error(
                        "Something went wrong while processing the report. Please try again."
                    )                 
    # ==========================================================
    # TAB 7 - Compare Reports
    # ==========================================================

    with tab7:

        st.subheader("📈 Compare Medical Reports")

        history_files = sorted(
            glob.glob("data/history/*.json")
        )

        if len(history_files) < 2:

            st.info(
                "Analyze at least two reports to compare them."
            )

        else:

            old_report = history_files[-2]
            new_report = history_files[-1]

            with open(old_report, "r", encoding="utf-8") as file:

                old_data = json.load(file)

            with open(new_report, "r", encoding="utf-8") as file:

                new_data = json.load(file)

            comparison_df = compare_reports(
                old_data["analysis"],
                new_data["analysis"]
            )

            st.success("Comparison generated successfully!")

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )
            st.divider()

            # ==========================================================
            # Footer
            # ==========================================================

            st.divider()

            st.markdown(
                """
            <div style="text-align:center; color:gray; font-size:14px;">

            🏥 <b>Medical Report AI Assistant</b><br><br>

            Built using <b>Python, Streamlit, OCR, Plotly & Gemini AI</b><br><br>

            © 2026 Souri Sarkar

            </div>
            """,
                unsafe_allow_html=True
            )