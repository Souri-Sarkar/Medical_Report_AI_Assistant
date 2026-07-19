import json


class MedicalAnalyzer:

    def __init__(self):

        with open(
            "models/normal_ranges.json",
            "r",
            encoding="utf-8"
        ) as file:

            self.ranges = json.load(file)

    def analyze(self, values):

        report = {}

        for parameter, value in values.items():

            if parameter not in self.ranges:
                continue

            low = self.ranges[parameter]["low"]
            high = self.ranges[parameter]["high"]
            unit = self.ranges[parameter]["unit"]

            # ----------------------------------
            # Determine Status
            # ----------------------------------

            if value < low:

                status = "Low"

            elif value > high:

                status = "High"

            else:

                status = "Normal"

            # ----------------------------------
            # Save Analysis
            # ----------------------------------

            report[parameter] = {

                "value": value,

                "unit": unit,

                "status": status,

                "low": low,

                "high": high,

                "normal_range": f"{low} - {high}"
            }

        return report