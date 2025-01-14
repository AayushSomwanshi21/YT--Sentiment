import React, { useEffect, useState } from 'react';
import axios from 'axios';


function App() {

  const [data, setData] = useState({});


  useEffect(() => {

    const handleResponse = async () => {

      const response = await axios.get('http://127.0.0.1:8000');
      console.log(response.data);
      setData(response.data)
    }

    handleResponse();

  }, [])

  return (
    <div>
      {data.average_sentiment_score}
    </div>
  );
}

export default App;
