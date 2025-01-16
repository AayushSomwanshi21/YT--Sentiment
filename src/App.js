import React, { useState } from 'react';
import axios from 'axios';
import SentimentPieChart from './components/SentimentPieChart';

function App() {

  const [data, setData] = useState({});

  const handleSubmit = async (e) => {

    e.preventDefault();
    const response = await axios.get('http://127.0.0.1:8000');
    console.log(response.data);
    setData(response.data)
  }



  return (
    <>
      <section className='heading'>
        Yotube Sentiment Anaylizer
      </section>
      <section className='form-container'>
        <form className="analyze-form" onSubmit={handleSubmit}>
          <input id="youtube-link" type="text" placeholder="Enter YouTube video link" />
          <div className='btn-container'>
            <button type="submit">Analyze</button>
          </div>
        </form>
      </section>
      {/*<section className='output-container'>
        <div>Positive Comments: {data.positive_comments}</div>
        <div>Negative Comments: {data.negative_comments}</div>
        <div>Avg Score: {data.average_sentiment_score}</div>
        <div>Sentiment: {data.overall_sentiment}</div>
      </section>*/}
      <section className='output-container'>
        {data.positive_comments && data.negative_comments && (
          <SentimentPieChart data={data} />
        )}
      </section>


    </>
  );
}

export default App;
