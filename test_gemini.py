from utils.ai_summary import generate_summary

analysis = {
    "Hemoglobin": {
        "value": 12,
        "status": "Low",
        "unit": "g/dL"
    },
    "WBC": {
        "value": 6.7,
        "status": "Normal",
        "unit": "thousand/uL"
    }
}

summary = generate_summary(
    patient_name="John Doe",
    report_type="CBC",
    analysis=analysis
)

print(summary)