from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# File path to store JSON data
data_file_path = 'data.json'

def read_data():
    try:
        with open(data_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        # If the file is not found, return an empty initial data
        return {"fields": []}

def write_data(data):
    with open(data_file_path, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/get_data', methods=['GET'])
def get_data():
    data = read_data()
    return jsonify(data)

@app.route('/save_data', methods=['POST'])
def save_data():
    if request.is_json:
        try:
            new_data = request.get_json()
            # Handle the new data as needed (e.g., update a database)
            print("Received data:", new_data)
            
            # Update the data in the file
            write_data(new_data)
            
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid JSON data"})

if __name__ == '__main__':
    app.run(debug=True)
