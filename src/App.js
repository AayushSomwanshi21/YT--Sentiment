import React, { useState } from 'react';
import axios from 'axios';
import SentimentPieChart from './components/SentimentPieChart';

function App() {

  const [data, setData] = useState({});
  const [link, setLink] = useState("");
  const [summary, setSummary] = useState([]);

  const handleChange = (e) => {
    setLink(e.target.value)
  }

  const handleSubmit = async (e) => {

    const parsedURL = new URL(link)
    let id = ""
    try {
      if (parsedURL.hostname.includes('youtube.com')) {
        id = parsedURL.searchParams.get('v');
      }
    } catch (error) {
      console.log(error);
    }

    e.preventDefault();
    const response = await axios.get(`http://127.0.0.1:8000/?id=${id}`);
    //console.log(response.data);
    setData(response.data)
    setSummary(response.data.summary_text);
  }



  return (
    <>
      <section className='heading'>
        Youtube Sentiment Anaylizer
      </section>
      <section className='form-container'>
        <form className="analyze-form" onSubmit={handleSubmit}>
          <input id="youtube-link" type="text" placeholder="Enter YouTube video link" value={link} onChange={handleChange} />
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
        <div className='video_display'>
          <img src={data.thumbnail_img} alt='thumbnail' style={{ height: "90%", width: '90%' }} />
          <div>{data.video_name}</div>
        </div>
        {data.positive_comments && data.negative_comments && (
          <SentimentPieChart data={data} />
        )}
      </section>
      {/* 
      <section>
        {summary.map((smry, index) => (
          <div key={index} style={{ color: 'white' }}>{smry}</div>
        ))}
      </section>

      */}


    </>
  );
}

export default App;
