from flask import Flask, request, jsonify,render_template
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, send_file
from io import BytesIO
app = Flask(__name__)

import json, io
def pivot_ui(df, outfile_path = "pivottablejs.html", url="",
    width="100%", height="500", **kwargs):
    with io.open(outfile_path, 'wt', encoding='utf8') as outfile:
        csv = df.to_csv(encoding='utf8')

    return  """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>PivotTable.js</title>

        <!-- external libs from cdnjs -->
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.11/c3.min.css">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.11/c3.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery-csv/0.71/jquery.csv-0.71.min.js"></script>


        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.19.0/pivot.min.css">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.19.0/pivot.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.19.0/d3_renderers.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.19.0/c3_renderers.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.19.0/export_renderers.min.js"></script>

        <style>
            body {font-family: Verdana;}
            .node {
              border: solid 1px white;
              font: 10px sans-serif;
              line-height: 12px;
              overflow: hidden;
              position: absolute;
              text-indent: 2px;
            }
            .c3-line, .c3-focused {stroke-width: 3px !important;}
            .c3-bar {stroke: white !important; stroke-width: 1;}
            .c3 text { font-size: 12px; color: grey;}
            .tick line {stroke: white;}
            .c3-axis path {stroke: grey;}
            .c3-circle { opacity: 1 !important; }
            .c3-xgrid-focus {visibility: hidden !important;}
        </style>
    </head>
    <body>
        <script type="text/javascript">
            $(function(){
                if(window.location != window.parent.location)
                    $("<a>", {target:"_blank", href:""})
                        .text("[pop out]").prependTo($("body"));

                $("#output").pivotUI(
                    $.csv.toArrays($("#output").text()),
                    $.extend({
                        renderers: $.extend(
                            $.pivotUtilities.renderers,
                            $.pivotUtilities.c3_renderers,
                            $.pivotUtilities.d3_renderers,
                            $.pivotUtilities.export_renderers
                            ),
                        hiddenAttributes: [""]
                    }, """+str(kwargs)+""")
                ).show();
             });
        </script>
        <div id="output" style="display: none;">"""+str(csv)+"""</div>
    </body>
</html>""" 
def show_user(url):
 #return  request.args.get('url', 'No URL provided')
 datas=[]
 # URL of the webpage to scrape
 p=1
 stop= False
 while not stop:
  url = url+":p:"+str(p)#request.path.split("/dash/")[-1]#"https://www.mubawab.ma/fr/sd/tanger/malabata/appartements-a-vendre"

# Send a GET request to fetch the page content
  response = requests.get(url)

# Check if the request was successful
  if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all divs with a specific class (replace 'your-class' with the actual class name)
    target_divs = soup.find_all("div", class_="listingBox")
    if len(target_divs)==0:
        stop=True
    else:
        p=p+1
    print(len(target_divs))
   
    # Iterate over each div and process its content
    for div in target_divs[:-1]:
       # print(len(div.find_all("a", class_="contactBtn")))
       
         
        datas.append({
"price":div.find_all(lambda tag: tag.has_attr('class') and any("priceTag" in cls for cls in tag['class']))[0].text.replace("\t","").replace("\n",""),            
"title":div.find_all(lambda tag: tag.has_attr('class') and any("listingTit" in cls for cls in tag['class']))[0].text.replace("\t","").replace("\n",""),

"location":div.find_all(lambda tag: tag.has_attr('class') and any("contactBar" in cls for cls in tag['class']))[0].text.replace("\t","").replace("\n",""),
"options":list(map(lambda a:a.text.replace("\n","").replace("\t"," "),list(div.find_all("div", class_="adDetailFeature")))),
"extras":list(map(lambda a:a.text.replace("\n","").replace("\t"," "),list(div.find_all("div", class_="adFeature"))))
            })  # Print the text inside the div
    
        # You can add more processing logic here
        print(len(datas))
  else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Convert to DataFrame
 df = pd.DataFrame(datas)
 return df
@app.route('/table')
def testert():
 return show_user(request.args.get('url', 'No URL provided')).to_html(index=False)
@app.route('/dash')
def testerd():
 return pivot_ui(show_user(request.args.get('url', 'No URL provided')))

@app.route('/download')
def download():
# return pivot_ui(show_user(request.args.get('url', 'No URL provided')))

    output = BytesIO()
    show_user(request.args.get('url', 'No URL provided')).to_excel(output, index=False)
    output.seek(0)
    
    # Return the Excel file as a response
    return send_file(output, as_attachment=True, download_name="data.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Export to Excel
# df.to_excel("output3.xlsx", index=False)

#print("Excel file saved successfully!")


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
  if type({}) ==type(data):
   if "fields" in data.keys() :
    for el in  data["fields"].copy():   
     if el=={} or el.get("value")=="":   
      data["fields"].remove(el)
        
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
