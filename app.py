from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample JSON data with input types
initial_data = {
    "fields": [
        {"label": "Field 1", "type": "text", "value": "Value 1"},
        {"label": "Field 2", "type": "dropdown", "options": ["Option 1", "Option 2"], "value": "Option 1"},
        {"label": "Field 3", "type": "radio", "options": ["Option A", "Option B"], "value": "Option A"},
        {"label": "Field 4", "type": "calendar", "value": "2023-01-01"},
        {"label": "Field 5", "type": "number", "value": 42}
    ]
}

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(initial_data)

@app.route('/save_data', methods=['POST'])
def save_data():
    if request.is_json:
        try:
            new_data = request.get_json()
            # Handle the new data as needed (e.g., update a database)
            print("Received data:", new_data)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid JSON data"})

if __name__ == '__main__':
    app.run(debug=True)
