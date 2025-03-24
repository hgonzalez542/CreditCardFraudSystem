import requests
import xml.etree.ElementTree as ET

API_KEY = "2N1TLDRCZLYATDONGWYHHCGQMGKCVFHM"
url = "https://api.fraudlabspro.com/v1/order/screen"

# POST data
data = {
    "key": API_KEY,
    "action": "CHECK",  # <-- Required to log the transaction
    "ip": "146.112.62.105",
    "bill_email": "test@example.com",
    "bill_phone": "1234567890",
    "bill_name": "John Doe",
    "bill_address": "123 Fake St",
    "bill_city": "Miami",
    "bill_state": "FL",
    "bill_country": "US",
    "bill_zip_code": "33101",
    "amount": "400.00",
    "currency": "USD",
    "card_bin": "411111",
    "user_order_id": "test-order-001",  # Optional but helps track in dashboard
    "user_order_memo": "Testing fraud check via API"
}

try:
    response = requests.post(url, data=data)

    print("Request URL:", response.url)
    print("Status Code:", response.status_code)

    if response.status_code == 200 and response.text.strip():
        root = ET.fromstring(response.text)

        print("\n--- Fraud Check Result (Logged to Dashboard) ---")
        print("Fraud Score        :", root.findtext("fraudlabspro_score"))
        print("Status             :", root.findtext("fraudlabspro_status"))
        print("Recommendation     :", root.findtext("fraudlabspro_status_desc"))
        print("High-Risk Country  :", root.findtext("is_high_risk_country"))
        print("Country Match      :", root.findtext("is_country_match"))
        print("Credits Remaining  :", root.findtext("fraudlabspro_credits"))
        print("Transaction ID     :", root.findtext("fraudlabspro_id"))
    else:
        print("❌ Error Response:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print("❌ Network Error:", e)
except ET.ParseError as pe:
    print("❌ XML Parsing Error:", pe)
    print("Raw Response:\n", response.text)