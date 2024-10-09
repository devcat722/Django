import React, { useState } from "react";
import DjangoUrl from "../constants";
import "./Home.css";

const Home = () => {
  // const [translatedText, setTranslatedText] = useState("");
  // const [medicalKeywords, setMedicalKeywords] = useState([]);
  // const [diagnosis, setDiagnosis] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [diagnosisData, setDiagnosisData] = useState(null); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Show loading spinner
    setError(null); // Reset error state

    try {
      // Make a POST request to the Django API endpoint
      const response = await fetch(`${DjangoUrl}/api/diagnose/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch diagnosis");
      }

      const data = await response.json();
      setDiagnosisData(data); // Store the API response data in state
    } catch (err) {
      setError(err.message); // Handle errors
    } finally {
      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div className="home-container">
      <header className="header">
        <h1>AI-Based Symptom Analysis & Diagnosis</h1>
      </header>

      <div className="prompt-section">
        <h2>Enter Patient's Prompt Below</h2>
        <form onSubmit={handleSubmit} className="prompt-form">
          {/* Updated from input to textarea */}
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type patient's symptoms..."
            rows="5" // You can adjust the rows to make it larger or smaller
          />
          <button type="submit">Get Diagnosis →</button>
        </form>
      </div>

      {/* Conditionally show loading spinner */}
      {loading && <p className="loading">Loading...</p>}

      {/* Show any error messages */}
      {error && <p className="error">{error}</p>}

      {/* Translated Text Section */}
      {diagnosisData && (
        <div className="diagnosis-results">
          <div className="translated-text-section">
            <h3>Translated Text:</h3>
            <p>{diagnosisData.translated_text}</p>
          </div>
          <div className="diagnosis-section">
            <h3>Symptom Diagnosis:</h3>
            <p>{diagnosisData.message}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>© 2024 Your Company. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default Home;