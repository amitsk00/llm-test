import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  // State for the conversation history
  const [chatHistory, setChatHistory] = useState([]);
  
  // Existing state
  const [currTokens, setTokens] = useState(null);
  const [currCost, setCost] = useState(null);
  const [message, setMessage] = useState(""); // User input
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  // Ref for auto-scrolling
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);


  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: message,
    };
    // Add user message to history
    setChatHistory(prev => [...prev, userMessage]);
    setMessage(""); // Clear input
    setLoading(true);

    try {
      const payload = {
        message: message,
        session_id: sessionId,
      };

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const result = await response.json();

      const aiMessage = {
        id: Date.now() + 1, // Simple unique ID
        sender: 'ai',
        text: result.answer,
      };
      // Add AI response to history
      setChatHistory(prev => [...prev, aiMessage]);

      setTokens(result.tokens);
      setCost(result.cost);
      if (result.session_id && !sessionId) {
        setSessionId(result.session_id);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        text: "Sorry, I encountered an error. Please try again."
      };
      setChatHistory(prev => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>Text2SQL App</h1>
      
      <div className="info-display">
        <span className="info-label">For last prompt --&#62; </span>
        <span className="info-label">Tokens used: </span>
        <span className="info-value tokens-value">{currTokens || 'NA'}</span>
        <span className="info-label">Cost: </span>
        <span className="info-value cost-value">${currCost || 'NA'}</span>
      </div>

      <div> <hr /> </div>

      <div className="chat-window">
        {chatHistory.map((msg) => (
          <div key={msg.id} className={`message-container ${msg.sender}`}>
            <div className="message">
              {msg.sender === 'ai' 
                ? <ReactMarkdown>{msg.text}</ReactMarkdown>
                : <p>{msg.text}</p>
              }
            </div>
          </div>
        ))}
        {loading && (
          <div className="message-container ai">
            <div className="message typing">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>


      <div> <hr /> </div>
      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type your query ..."
          className="query-input"
        />
        <button onClick={sendMessage} disabled={loading || !message.trim()} className="send-button">
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
