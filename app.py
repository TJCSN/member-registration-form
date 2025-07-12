from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

CSV_FILE = 'data.csv'

def read_csv():
    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(data):
    with open(CSV_FILE, 'w', newline='') as f:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/')
def form():
    users = read_csv()
    names = [user['FullName'] for user in users]
    return render_template('form.html', names=names)

@app.route('/get_user', methods=['POST'])
def get_user():
    selected_name = request.json['name']
    users = read_csv()
    for user in users:
        if user['FullName'] == selected_name:
            return jsonify(user)
    return jsonify({})

@app.route('/submit', methods=['POST'])
def submit():
    updated_data = request.json
    users = read_csv()
    for i, user in enumerate(users):
        if user['FullName'] == updated_data['FullName']:
            users[i] = updated_data
            break
    else:
        users.append(updated_data)
    write_csv(users)
    return jsonify({'status': 'success'})
