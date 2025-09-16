import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

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

      // console.log("12" , response)
      // // console.log("-----")
      // console.log("34" , result.tokens)
      // console.log("34" , result.cost)

      // console.log("API response :", result);

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
          style={{ padding: "8px", width: "60%" }}
        />
        <button onClick={sendMessage} disabled={loading || !message.trim()} style={{ marginLeft: "8px", padding: "8px" }}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
      {data && (
        <div style={{
          background: "#e0e0e0",
          padding: "10px 16px",
          borderRadius: "16px",
          maxWidth: "60%",
          margin: "12px 0" ,
          marginLeft: "auto",      
          display: "block"   
        }}>
            <div style={{ color: 'red', fontWeight: 'bold' }}>Tokens used: {currTokens}</div>
            <div style={{ color: 'red', fontWeight: 'bold' }}>Cost: {currCost}</div>          
            <div><ReactMarkdown>{data}</ReactMarkdown></div>

           {/* {JSON.stringify(data)} */}
        </div>
      )}
    </div>
  );
}

export default App;
