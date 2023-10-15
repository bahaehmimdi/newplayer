from flask import Flask, request, jsonify,render_template
import json

app = Flask(__name__)
@app.route('/edit_data', methods=['GET', 'POST'])
def edit_data():
    if request.method == 'POST':
        try:
            # Read the updated data from the HTML form
            updated_data = {
                "fields": []
            }
            for key, value in request.form.items():
                field_info = key.split('_')
                index = int(field_info[1])
                field_type = field_info[0]

                # Ensure the index is within bounds
                while index >= len(updated_data["fields"]):
                    updated_data["fields"].append({})

                if field_type == 'label':
                    updated_data["fields"][index]["label"] = value
                elif field_type == 'type':
                    updated_data["fields"][index]["type"] = value
                elif field_type == 'options':
                    updated_data["fields"][index]["options"] = value.split(',')
                elif field_type == 'value':
                    updated_data["fields"][index]["value"] = value
                else:
                    updated_data["fields"].pop()
            "fields"
            # Update the data in the file
            write_data(updated_data)

            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        # Read the current data to display in the HTML form
        current_data = read_data()
        return render_template('edit_data.html', current_data=current_data)



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
  if  len(data)>0:  
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
