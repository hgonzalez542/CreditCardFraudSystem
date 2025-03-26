import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [form, setForm] = useState({
    ip: '',
    bill_email: '',
    bill_name: '',
    bill_phone: '',
    bill_address: '',
    bill_city: '',
    bill_state: '',
    bill_country: '',
    bill_zip_code: '',
    amount: '',
    currency: 'USD',
    card_bin: ''
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post('http://localhost:5000/check-fraud', form);
    setResult(res.data);
  };

  return (
    <div className="App">
      <h1>Fraud Check</h1>
      <form onSubmit={handleSubmit}>
        {Object.keys(form).map((key) => (
          <div key={key}>
            <label>{key}:</label>
            <input name={key} value={form[key]} onChange={handleChange} />
          </div>
        ))}
        <button type="submit">Check Fraud</button>
      </form>

      {result && (
        <div>
          <h2>Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
