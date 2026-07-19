from dotenv import load_dotenv
from google.genai import Client
import os
import time

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------
load_dotenv()

# ---------------------------------------
# Initialize Gemini Client
# ---------------------------------------
client = Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_summary(patient_name, report_type, analysis):
    """
    Generate an AI-powered medical report summary.
    """

    # Convert analysis dictionary into readable text
    report = ""

    for parameter, details in analysis.items():

        report += (
            f"{parameter}: "
            f"{details['value']} {details['unit']} "
            f"({details['status']})\n"
        )

    prompt = f"""
You are an experienced physician and medical report assistant.

Patient Name: {patient_name}

Report Type: {report_type}

Medical Test Results:

{report}

Your task is to explain the report in very simple language that a non-medical person can understand.

Return the response in EXACTLY the following format.

# 🩺 Overall Report Summary
Write 4-6 lines summarizing the patient's health.

# 📋 Test Interpretation
Explain every parameter one by one.

For each parameter include:
• What it measures
• Whether it is Normal / High / Low
• Why it matters

# ⚠ Abnormal Findings
List ONLY abnormal parameters.
If everything is normal, clearly mention that.

# 🥗 Lifestyle Recommendations
Provide at least 5 personalized recommendations.

Examples:
• Foods to eat
• Foods to avoid
• Exercise
• Hydration
• Sleep
• Stress management

# 👨‍⚕️ When to Consult a Doctor
Mention situations where the patient should seek medical advice.

# 📌 Disclaimer
Mention that this report is AI-generated and is not a substitute for professional medical advice.

Do NOT prescribe medicines.
Use simple English.
Use bullet points wherever possible.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if attempt < 2:
                time.sleep(5)

            else:

                return f"""
## ⚠ AI Summary Unavailable

The AI service is temporarily busy.

Reason:

{str(e)}

Please try again after a few minutes.
"""