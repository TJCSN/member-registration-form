from flask import Flask, render_template, request, redirect, url_for
import csv, os
from datetime import datetime

app = Flask(__name__)

# Ensure CSV has correct headers
def ensure_csv_headers(filename, expected_headers):
    if not os.path.exists(filename):
        return

    with open(filename, mode='r', newline='', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if not rows:
        return

    actual_headers = rows[0]
    if actual_headers != expected_headers:
        print("⚠️ Fixing CSV headers...")
        data_rows = rows[1:] if len(rows) > 1 else []
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(expected_headers)
            writer.writerows(data_rows)

# Load race options from races.csv
def load_race_options():
    race_list = []
    if os.path.exists('races.csv'):
        try:
            with open('races.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                race_list = [row["RaceName"] for row in reader if row.get("RaceName")]
        except UnicodeDecodeError:
            with open('races.csv', mode='r', newline='', encoding='latin-1') as file:
                reader = csv.DictReader(file)
                race_list = [row["RaceName"] for row in reader if row.get("RaceName")]
    return race_list

@app.route('/')
def start_page():
    return render_template('start.html')

@app.route('/new_registration')
def new_registration():
    return render_template('member_registration.html')

@app.route('/race_registration')
def race_registration():
    filename = 'data.csv'
    names = []

    if os.path.exists(filename):
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                names = [row["Name"] for row in reader if "Name" in row]
        except UnicodeDecodeError:
            with open(filename, mode='r', newline='', encoding='latin-1') as file:
                reader = csv.DictReader(file)
                names = [row["Name"] for row in reader if "Name" in row]

    races = load_race_options()
    return render_template('race_registration.html', names=names, races=races)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_data = {
        "Timestamp": timestamp,
        "Name": request.form.get("FullName"),
        "IC": request.form.get("IC") or "",
        "Email": request.form.get("Email"),
        "Gender": request.form.get("Gender"),
        "Nationality": request.form.get("Nationality"),
        "Race": request.form.get("Race"),
        "DOB": request.form.get("DOB"),
        "Age": request.form.get("Age"),
        "Category": request.form.get("Category"),
        "ContactNumber": request.form.get("ContactNumber"),
        "RowingSide": request.form.get("RowingSide"),
        "Weight": request.form.get("Weight"),
        "JerseySize": request.form.get("JerseySize"),
        "SDBACard": request.form.get("SDBACard"),
        "Helms": request.form.get("Helms"),
        "CoachCert": request.form.get("CoachCert"),
        "SwimAbility": request.form.get("SwimAbility"),
        "MedicalHistory": request.form.get("MedicalHistory"),
        "ECName": request.form.get("ECName"),
        "ECRelationship": request.form.get("ECRelationship"),
        "ECContact": request.form.get("ECContact")
    }

    filename = 'data.csv'
    header = list(new_data.keys())
    rows = []

    ensure_csv_headers(filename, header)

    if os.path.exists(filename):
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
        except UnicodeDecodeError:
            with open(filename, mode='r', newline='', encoding='latin-1') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

    updated = False
    for row in rows:
        if row.get("Name") == new_data["Name"]:
            for key in new_data:
                if new_data[key]:  # only overwrite if new value is not blank
                    row[key] = new_data[key]
            updated = True
            break

    if not updated:
        rows.append(new_data)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    
    return f"✅ Thank you, {new_data['Name']}! You have successfully registered for {new_data['Race']}."


if __name__ == '__main__':
    app.run(debug=True)
