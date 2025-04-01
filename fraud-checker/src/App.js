import React, { useState } from "react";
import axios from "axios";
import "./App.css";

// Function includes the set parameters for the webpage itself
function App() {
  const [form, setForm] = useState({
    ip: "",
    bill_email: "",
    bill_name: "",
    bill_phone: "",
    bill_address: "",
    bill_city: "",
    bill_state: "",
    bill_country: "",
    bill_zip_code: "",
    amount: "",
    currency: "USD",
    card_bin: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // the function handles the submission of the form and sends the data to the server for processing
  // It also handles the loading state and error messages
  // and updates the result state with the response from the server
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setErrorMsg("");

    try {
      const response = await axios.post("http://localhost:5000/check-fraud", form);
      setResult(response.data);
    } catch (error) {
      console.error("Error during fraud check:", error);

      if (error.response && error.response.data) {
        setErrorMsg(error.response.data.error || "An unknown error occurred.");
      } else {
        setErrorMsg("Failed to connect to the server.");
      }
    } finally {
      setLoading(false);
    }
  };

  // The function renders the form and the result of the fraud check
  // It includes input fields for the user to enter their information
  // and a button to submit the form
  return (
    <div className="app-container">
      <div className="form-container">
        <h1>Fraud Check</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            {Object.keys(form).map((key) => (
              <div className="form-group" key={key}>
                <label className="form-label">
                  {key.replace(/_/g, " ").toUpperCase()}:
                </label>
                <input
                  name={key}
                  value={form[key]}
                  onChange={handleChange}
                  className="form-input"
                  required={["bill_email", "amount"].includes(key)}
                />
              </div>
            ))}
          </div>
          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? "Checking..." : "Check Fraud"}
          </button>
        </form>

        {errorMsg && (
          <div className="error-box">
            <strong>Error:</strong> {errorMsg}
          </div>
        )}

        {result && (
          <div className="result-container">
            <h2>Result:</h2>
            <pre className="result-box">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
