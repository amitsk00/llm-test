// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


// In a React component file (e.g., App.js)

import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Make the API call to your FastAPI backend
    const message = "cricket"
    // fetch('http://localhost:8000/chat/${message}')
    fetch('http://localhost:8000/chat/cricket')
      .then(response => {
              // console.log("test1"  , response) 
              return response.json()
            })
      .then(data => {
          // console.log(response)
          // console.log("test data" , data )
          setData(data)
        })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  // return (
  //   <div>
  //     <h1>React App</h1>
  //     {data ? (
  //       <p>Message from backend: {JSON.stringify(data)}</p>
  //     ) : (
  //       <p>Loading...</p>
  //     )}
  //   </div>
  // );


  return (
    <div>
      <h1>React App</h1>
      {data ? (
        <div style={{
          background: "#e0e0e0",
          padding: "10px 16px",
          borderRadius: "16px",
          maxWidth: "60%",
          margin: "12px 0"
        }}>
          {JSON.stringify(data)}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );

}

export default App;


// const res = await fetch("http://127.0.0.1:8000/chat", {
//   method: "POST",
//   headers: { "Content-Type": "application/json" },
//   body: JSON.stringify({ messages: newMessages }),
// });


