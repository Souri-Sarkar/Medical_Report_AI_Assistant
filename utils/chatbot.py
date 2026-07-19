from dotenv import load_dotenv
from google.genai import Client
import os
import time

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Initialize Gemini Client
# --------------------------------------------------

client = Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Medical AI Chat Function
# --------------------------------------------------

def ask_medical_ai(question, report_text, analysis):

    prompt = f"""
You are an experienced medical AI assistant.

The patient has uploaded a medical report.

==================================================
PATIENT REPORT
==================================================
{report_text}

==================================================
EXTRACTED ANALYSIS
==================================================
{analysis}

==================================================
PATIENT QUESTION
==================================================
{question}

Instructions:

1. Answer ONLY using the uploaded report and extracted analysis.
2. Mention the patient's actual values.
3. Explain whether each value is Normal, High, or Low.
4. If abnormal, explain the possible reasons in simple language.
5. These are possible causes only, not a diagnosis.
6. Suggest healthy foods and lifestyle improvements.
7. Never prescribe medicines.
8. Never diagnose diseases.
9. Keep the answer under 180 words.
10. Use simple English.
11. Use bullet points.

Always respond in this format:

## Answer

(Simple explanation)

## Possible Reasons

• Reason 1

• Reason 2

• Reason 3

## Lifestyle Advice

• Advice 1

• Advice 2

• Advice 3

## Disclaimer

This response is AI-generated and is for educational purposes only.
It is not a substitute for professional medical advice.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )

            if response.text:
                return response.text.strip()

            return "Sorry, I couldn't generate an answer."

        except Exception as e:

            if attempt < 2:
                time.sleep(5)

            else:
                return f"❌ Gemini Error:\n\n{str(e)}"


# --------------------------------------------------
# Debug - List Available Gemini Models
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("Gemini Model Checker")
    print("=" * 60)

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        print("✅ API Key Loaded Successfully")
    else:
        print("❌ GEMINI_API_KEY not found in .env")

    print("\nListing available Gemini models...\n")

    try:

        for model in client.models.list():
            print(model.name)

    except Exception as e:

        print("\n❌ Error while listing models:")
        print(e)