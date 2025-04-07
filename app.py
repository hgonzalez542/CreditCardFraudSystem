# Code is written and maintained by Hector Gonzalez
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

#APi Key and URL for FraudLabs Pro
API_KEY = "ZQTTQZZISHUTC9MGW0AJ7DOFFP2OVYDH"
FRAUDLABS_URL = "https://api.fraudlabspro.com/v1/order/screen"

# Set up the Flask app
# Route for the main page
@app.route("/check-fraud", methods=["POST"])
def check_fraud():
    # Validate the request method
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        # Required fields
        bill_email = data.get("bill_email")
        amount = data.get("amount")

        if not bill_email or not amount:
            return jsonify({"error": "Missing required fields: bill_email and amount are required."}), 400
        # all the parameters that are going to be sent to the FraudLabs Pro API
        payload = {
            "key": API_KEY,
            "ip": data.get("ip") or "146.112.62.105", # Default IP
            "bill_email": bill_email,
            "bill_name": data.get("bill_name", ""),
            "bill_phone": data.get("bill_phone", ""),
            "bill_address": data.get("bill_address", ""),
            "bill_city": data.get("bill_city", ""),
            "bill_state": data.get("bill_state", ""),
            "bill_country": data.get("bill_country", ""),
            "bill_zip_code": data.get("bill_zip_code", ""),
            "amount": amount,
            "currency": data.get("currency", "USD"),
            "card_bin": data.get("card_bin", "")
        }

        print("Sending to FraudLabs Pro:", payload)

        # Send GET request
        response = requests.get(FRAUDLABS_URL, params=payload)
        content_type = response.headers.get("Content-Type", "")

        # Try parsing JSON
        if "application/json" in content_type:
            response_data = response.json()
            print("JSON response:", response_data)
            return jsonify(response_data), response.status_code

        # Parse XML if needed
        elif "application/xml" in content_type or "text/xml" in content_type:
            print("**Received XML response.**")
            root = ET.fromstring(response.text)
            parsed_data = {child.tag: child.text for child in root}
            print("**Parsed XML response:**", parsed_data)
            return jsonify(parsed_data), response.status_code

        # Fallback if unknown content
        else:
            print("Unexpected content type:", content_type)
            return jsonify({
                "error": "Unknown response format from FraudLabs Pro",
                "raw_response": response.text
            }), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
