import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [currTokens, setTokens] = useState(null);
  const [currCost, setCost] = useState(null);
  const [message, setMessage] = useState(""); // User input
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/chat/${encodeURIComponent(message)}`);
      const result = await response.json();

      setData(result.answer);
      setTokens(result.tokens);
      setCost(result.cost) ;
    } catch (error) {
      console.error('Error fetching data:', error);
      setData({ error: "Failed to fetch response" });
    }
    setLoading(false);
  };

  return (
    <div>
      <h1>Text2SQL App</h1>
      <div style={{ marginBottom: "16px" }}>
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type your query ..."
          className="query-input"
        />
        <button onClick={sendMessage} disabled={loading || !message.trim()} className="send-button">
          {loading ? "Sending..." : "Send"}
        </button>
      </div>

      <div className="info-display">
        <span className="info-label">Tokens used: </span>
        <span className="info-value tokens-value">{currTokens}</span>
        <span className="info-label">    </span>
        <span className="info-label">Cost: </span>
        <span className="info-value cost-value">{currCost}</span>
        <span className="info-label">   --- </span>
      </div>

      {data && (
        <div className="response-container">
            <div><ReactMarkdown>{data}</ReactMarkdown></div>

           {/* {JSON.stringify(data)} */}
        </div>
      )}
      <hr />
    </div>
  );
}

export default App;
