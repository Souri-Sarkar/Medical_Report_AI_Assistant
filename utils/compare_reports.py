import pandas as pd


def compare_reports(old_analysis, new_analysis):

    comparison = []

    parameters = set(old_analysis.keys()) | set(new_analysis.keys())

    for parameter in sorted(parameters):

        old = old_analysis.get(parameter)

        new = new_analysis.get(parameter)

        old_value = old["value"] if old else None
        new_value = new["value"] if new else None

        if old_value is not None and new_value is not None:

            difference = round(new_value - old_value, 2)

            if difference > 0:
                trend = "⬆ Improved"

            elif difference < 0:
                trend = "⬇ Decreased"

            else:
                trend = "➡ No Change"

        else:

            difference = "-"

            trend = "N/A"

        comparison.append({

            "Parameter": parameter,

            "Previous": old_value,

            "Current": new_value,

            "Difference": difference,

            "Trend": trend

        })

    return pd.DataFrame(comparison)