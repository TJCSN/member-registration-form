from flask import Flask, render_template, request, redirect
import csv, os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'data.csv'
RACE_FILE = 'races.csv'

def load_race_options():
    race_list = []
    if os.path.exists(RACE_FILE):
        with open(RACE_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            race_list = [row.get("RaceName", "").strip() for row in reader if row.get("RaceName")]
    return race_list

@app.route('/')
def start_page():
    return render_template('start.html')

@app.route('/new_registration')
def new_registration():
    return render_template('member_registration.html')

@app.route('/race_registration')
def race_registration():
    members = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            members = list(reader)
    races = load_race_options()
    return render_template('race_registration.html', members=members, races=races)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    form_type = request.form.get("FormType", "member")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    full_name = request.form.get("FullName") or request.form.get("Name", "")

    new_data = {
        "Timestamp": timestamp,
        "FormType": form_type,
        "FullName": full_name,
        "PreferredName": request.form.get("PreferredName", ""),
        "IC": request.form.get("IC", ""),
        "Gender": request.form.get("Gender", ""),
        "DOB": request.form.get("DOB", ""),
        "Nationality": request.form.get("Nationality", ""),
        "Race": request.form.get("Race", ""),
        "ContactNumber": request.form.get("ContactNumber", ""),
        "Email": request.form.get("Email", ""),
        "PostalCode": request.form.get("PostalCode", ""),
        "Weight": request.form.get("Weight") or request.form.get("WeightFromMember", ""),
        "JerseySize": request.form.get("JerseySize", ""),
        "MedicalHistory": request.form.get("MedicalHistory", ""),
        "ECName": request.form.get("ECName", ""),
        "ECRelationship": request.form.get("ECRelationship", ""),
        "ECContact": request.form.get("ECContact", ""),
        "Paddling Side - Left": request.form.get("PaddlingSideLeft", "No"),
        "Paddling Side - Right": request.form.get("PaddlingSideRight", "No"),
        "Helms": request.form.get("Helms", ""),
        "CoachCert": request.form.get("CoachCert", ""),
        "SwimAbility": request.form.get("SwimAbility", ""),
        "SDBACard": request.form.get("SDBACard", "")
    }

    if form_type == "race":
        for field in ["Available_Day1_AM", "Available_Day1_PM", "Available_Day2_AM", "Available_Day2_PM"]:
            value = request.form.get(field)
            if value:
                new_data[field] = value

    # Update or append to data.csv
    fieldnames = list(new_data.keys())
    rows = []
    found = False

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("FullName") == full_name:
                    for key in new_data:
                        if new_data[key]:  # Only overwrite if value is provided
                            row[key] = new_data[key]
                    found = True
                rows.append(row)

    if not found:
        rows.append(new_data)

    # Write to CSV with header only once
    write_header = not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)

    # Show summary only for member form
    if form_type == "member":
        def format_section(title, keys):
            items = [f"<li><strong>{key}:</strong> {new_data.get(key)}</li>"
                     for key in keys if new_data.get(key)]
            return f"<h3>{title}</h3><ul>{''.join(items)}</ul>" if items else ""

        personal_info = [
            "FullName", "PreferredName", "IC", "Gender", "DOB", "Nationality",
            "Race", "ContactNumber", "Email", "PostalCode", "Weight", "JerseySize"
        ]
        emergency = ["ECName", "ECRelationship", "ECContact"]
        certifications = [
            "Paddling Side - Left", "Paddling Side - Right", "Helms",
            "CoachCert", "SwimAbility", "SDBACard"
        ]

        return f"""
        <!DOCTYPE html>
        <html><head><title>Member Registration Summary</title></head>
        <body style="font-family:Arial;max-width:600px;margin:auto">
          <h2>✅ Thank you, {new_data.get('FullName', 'Participant')}!</h2>
          <p>You’ve successfully registered as a member.</p>
          {format_section("👤 Personal Details", personal_info)}
          {format_section("🚨 Emergency Contact", emergency)}
          {format_section("📜 Certifications & Experience", certifications)}
          <a href="/">🏠 Back to Home</a>
        </body></html>
        """
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)