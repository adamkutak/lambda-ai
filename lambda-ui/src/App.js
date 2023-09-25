import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Assuming your Flask app is running on localhost:5000
    axios.get('http://localhost:5000/')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.log('Error fetching data:', error);
      });
  }, []);

  return (
    <div className="App">
      <h1>React + Flask</h1>
      {data ? <p>{data.message}</p> : 'Loading...'}
    </div>
  );
}

export default App;