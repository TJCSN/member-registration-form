from flask import Flask, request, render_template
import csv, os

app = Flask(__name__)
DATA_FILE = 'data.csv'

# These match the form field names from form.html
FIELD_NAMES = [
    "FullName", "Email", "Gender", "Nationality", "Race", "DOB", "Age", "Category",
    "ContactNumber", "RowingSide", "Weight", "JerseySize", "SDBACard", "Helms",
    "CoachCert", "SwimAbility", "MedicalHistory", "ECName", "ECRelationship", "ECContact"
]

@app.route('/', methods=['GET', 'POST'])
def form():
    selected_name = ''
    existing_data = {}

    if request.method == 'POST':
        selected_name = request.form.get("FullName", "")

        # User clicked "Load Info" button
        if 'load' in request.form:
            existing_data = load_existing_data(selected_name)
        else:
            # User submitted form, so save their updates
            save_data(request.form)

    return render_template('form.html', data=existing_data, selected_name=selected_name)

def load_existing_data(name):
    """Find and return data for the selected name."""
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("FullName") == name:
                return row
    return {}

def save_data(form):
    """Update or add new data based on FullName."""
    rows = []
    updated = False
    new_row = {field: form.get(field, '') for field in FIELD_NAMES}
    name = new_row["FullName"]

    # Load existing data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["FullName"] == name:
                    rows.append(new_row)  # Replace old data
                    updated = True
                else:
                    rows.append(row)

    if not updated:
        rows.append(new_row)  # Add new entry

    # Write back to CSV
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(rows)

@app.route('/export')
def export():
    """View contents of data.csv in browser (plain text)."""
    if not os.path.exists(DATA_FILE):
        return "No data available.", 404
    with open(DATA_FILE, 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)
