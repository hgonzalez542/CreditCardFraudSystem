from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)  # Allows your React frontend to make requests

API_KEY = "2N1TLDRCZLYATDONGWYHHCGQMGKCVFHM"
API_URL = "https://api.fraudlabspro.com/v1/order/screen"

@app.route('/check-fraud', methods=['POST'])
def check_fraud():
    data = request.json
    data['key'] = API_KEY
    data['action'] = "CHECK"

    try:
        response = requests.post(API_URL, data=data)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            result = {
                "score": root.findtext("fraudlabspro_score"),
                "status": root.findtext("fraudlabspro_status"),
                "recommendation": root.findtext("fraudlabspro_status_desc"),
                "country_match": root.findtext("is_country_match"),
                "high_risk_country": root.findtext("is_high_risk_country"),
                "credits": root.findtext("fraudlabspro_credits")
            }
            return jsonify(result)
        else:
            return jsonify({"error": "FraudLabs Pro error", "response": response.text}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
