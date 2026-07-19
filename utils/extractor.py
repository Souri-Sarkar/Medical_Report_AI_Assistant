import re


class MedicalExtractor:

    def __init__(self):

        self.parameters = {
            "Hemoglobin": ["hemoglobin", "haemoglobin", "hb"],
            "RBC": ["rbc count", "rbc"],
            "WBC": ["total leucocyte count", "wbc"],
            "Platelets": ["platelet count", "platelets", "plt"],
            "HCT": ["hematocrit", "hct"],
            "MCV": ["mcv"],
            "MCH": ["mch"],
            "MCHC": ["mchc"],
            "ESR": ["esr"]
        }

    def extract(self, text):

        results = {}

        lines = text.split("\n")

        for line in lines:

            clean_line = " ".join(line.split())
            lower = clean_line.lower()

            for parameter, keywords in self.parameters.items():

                for keyword in keywords:

                    if keyword in lower:

                        # Find the text AFTER the keyword only
                        after = lower.split(keyword, 1)[1]

                        numbers = re.findall(r"\d+(?:\.\d+)?", after)

                        for num in numbers:

                            value = float(num)

                            if value > 1900:
                                continue

                            results[parameter] = value
                            break

                        break

        return results