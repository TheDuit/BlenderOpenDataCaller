from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(*)

@app.route('/api/blenderData', methods=['GET'])
def get_blender_data():
    blender_api_url = "https://opendata.blender.org/benchmarks/query/?group_by=device_name&group_by=compute_type&response_type=datatables"
    
    try:
        response = requests.get(blender_api_url)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Failed to fetch data from Blender API. Status code: {response.status_code}"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8042, debug=False)
