# 💳 Real-Time Credit Card Fraud Detection Web App

This is a full-stack web application that detects potentially fraudulent credit card transactions in real time using the [FraudLabs Pro API](https://www.fraudlabspro.com). The project simulates a real-world fraud detection workflow used by financial institutions, with a modern frontend built in React.js and a backend developed using Python Flask.

---

## 🔧 Tech Stack

| Layer       | Technology           |
|-------------|----------------------|
| Frontend    | React.js (Axios, JSX)|
| Backend     | Python + Flask       |
| API Service | FraudLabs Pro API    |
| IDE         | Visual Studio Code   |

---

## 📦 Features

- Collects credit card transaction data from the user
- Sends the data to the backend securely
- Flask backend sends a POST request to FraudLabs Pro API
- Parses XML response from the API
- Returns fraud analysis to the React frontend
- Displays:
  - Fraud score
  - Risk status (APPROVE, REVIEW, REJECT)
  - Country match & high-risk flags
  - Remaining API credits
- Automatically logs the transaction to the FraudLabs Pro dashboard

---

## 📡 API Details

- **Endpoint Used:** `https://api.fraudlabspro.com/v1/order/screen`
- **API Format:** XML response
- **Fields Sent:**
  - IP address
  - Email
  - Phone number
  - Billing address
  - Amount
  - Card BIN (first 6 digits)
- **Required param:** `action=CHECK` to log transaction

---

## 🧠 How It Works

1. **React Form** collects user input.
2. On submit, **Axios** sends the transaction data to the Flask backend.
3. Flask sends a `POST` request to the FraudLabs Pro API with `action=CHECK`.
4. The API returns an **XML response** with fraud risk details.
5. Flask parses the XML using `ElementTree` and returns a clean JSON.
6. **React displays** the fraud result and the transaction is also visible in your [FraudLabs Pro Dashboard](https://www.fraudlabspro.com/merchant/dashboard).

---

## 🖥️ Local Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/fraud-detection-app.git
cd fraud-detection-app
