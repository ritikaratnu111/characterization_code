from openpyxl import Workbook

# Sample data
data = {
    "Experiment1": {
        "Component1": {
            "active": {"internal": 1, "switching": 1, "leakage": 1},
            "inactive": {"internal": 0, "switching": 0, "leakage": 0}
        },
        "Component2": {
            "active": {"internal": 2, "switching": 2, "leakage": 2},
            "inactive": {"internal": 0, "switching": 0, "leakage": 0}
        },
        "Component3": {
            "active": {"internal": 3, "switching": 3, "leakage": 3},
            "inactive": {"internal": 6, "switching": 4, "leakage": 3}
        }
    },
    # Add more experiments if needed
}

wb = Workbook()
sheet = wb.active

# Write headers
headers = ["Experiments", "", "", "", "", "", "", "", ""]
sheet.append(headers)

sub_headers = ["", "Component1", "", "", "", "", "", "Component2", "", "", "", "", "", "Component3", "", "", "", "", ""]
sheet.append(sub_headers)

sub_sub_headers = ["", "Active", "", "", "Inactive", "", "", "Active", "", "", "Inactive", "", "","Active", "", "", "Inactive", "", ""]
sheet.append(sub_sub_headers)

power_types = ["", "internal", "switching", "leakage", "internal", "switching", "leakage", "internal", "switching", "leakage", "internal", "switching", "leakage", "internal", "switching", "leakage", "internal", "switching", "leakage" ] 
sheet.append(power_types)

# Write data to the sheet
for experiment, components in data.items():
    row = [experiment]
    for component in ["Component1", "Component2", "Component3"]:
        for status in ["active", "inactive"]:
            powers = components[component][status]
            row.extend([powers.get("internal", ""), powers.get("switching", ""), powers.get("leakage", "")])
    sheet.append(row)

# Merge cells for sub-columns
for i in range(2, 4):
    sheet.merge_cells(start_row=1, start_column=i * 4 - 2, end_row=1, end_column=i * 4 + 1)

# Save the workbook
wb.save("experiment_data.xlsx")
