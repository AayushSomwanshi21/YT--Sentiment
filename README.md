# YouTube Comment Summarizer 🎥🧠

An AI-powered web application that fetches comments from any YouTube video and generates a sentiment-aware summary using NLP models. Ideal for users looking to quickly understand public opinion without sifting through hundreds of comments.

---

## 🚀 Features

- 🔍 Fetch comments from any YouTube video using YouTube Data API
- 🧠 Summarize comments using HuggingFace's `facebook/bart-large-cnn` model
- 😊 Analyze overall sentiment (positive, neutral, negative)
- ⚡ Fast and responsive UI with React.js and shadcn/ui
- 🧩 Backend built with FastAPI for efficient API handling

---

## 🛠️ Tech Stack

### Frontend
- **React.js** – Modern JavaScript library for building user interfaces
- **shadcn/ui** – Clean, accessible components for a better UI/UX

### Backend
- **FastAPI** – High-performance Python framework for API development
- **HuggingFace Transformers** – NLP model for summarization
- **YouTube Data API** – To fetch video comments programmatically

---

## 📦 Installation

### Prerequisites
- Node.js
- Python 3.8+
- YouTube API Key
- HuggingFace Token

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-comment-summarizer.git
cd youtube-comment-summarizer
```

### 2. Setup Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Create a .env file with:

```ini
YOUTUBE_API_KEY=your_youtube_api_key
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

### 3. Setup Frontend (React.js)

```bash
cd frontend
npm install
npm run dev
```

## 🧪 Example Use Case

- Enter a valid YouTube video URL.

- The app fetches the top 100 comments based on like counts and replies.
 
- The sentiment of comments is displayed (positive and negative comments percentage).

## 📸 Screenshot

**Home Page where the user pastes the YouTube video url and the a Pie Chart of sentiment analysis is displayed with the percentage of positive and negative sentiments**

![Main Page](public/screeenshots/Screenshot%202025-05-03%20144550.png)


## 💬 Acknowledgements

- HuggingFace Transformers

- FastAPI

- YouTube Data API

- shadcn/ui
