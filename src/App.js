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
    <>
      <section className='heading'>
        Yotube Sentiment Anaylizer
      </section>
      <section className='form-container'>
        <form className="analyze-form">
          <input id="youtube-link" type="text" placeholder="Enter YouTube video link" />
          <div className='btn-container'>
            <button type="submit">Analyze</button>
          </div>

        </form>
      </section>


      {data.average_sentiment_score}
    </>
  );
}

export default App;
