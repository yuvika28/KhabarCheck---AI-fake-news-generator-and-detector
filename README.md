# 🔎 KhabarCheck – Truth Lens

KhabarCheck is an AI-powered web application that can **generate fake news articles and detect whether news is real or fake**.

The project combines **Machine Learning for fake news detection** with **Generative AI (Google Gemini)** for article generation, wrapped inside an interactive **Streamlit web interface**.

This project demonstrates how **NLP, Machine Learning, and Generative AI** can work together to understand and analyze misinformation.

---

# ✨ Features

## 📝 Fake News Article Generator

* Generates **realistic fake news articles** based on a topic.
* Uses **Google Gemini API**.
* Each article includes:

  * Newspaper-style headline
  * Fake quotes
  * Statistics
  * 200–300 words of content.

## 🔍 Fake News Detection

* Users can paste any news text.
* The ML model predicts whether it is:

  * ✅ **Real News**
  * ❌ **Fake News**
* Displays **confidence score** using a visual progress bar.

## 🎨 Modern UI

Built using **Streamlit** with custom CSS:

* Gradient headers
* Rounded input fields
* Card-style UI blocks
* Animated buttons

---

# 🧠 Tech Stack

* Python
* Streamlit
* Scikit-learn
* Pandas
* Joblib
* Google Gemini API
* python-dotenv

---

# 📂 Project Structure

```
KhabarCheck/
│
├── app.py                # Main Streamlit application
├── model.pkl             # Trained fake news detection model
├── .env                  # API key file (not pushed to GitHub)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

# ⚙️ Installation

## 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/khabarcheck.git
cd khabarcheck
```

## 2️⃣ Create a virtual environment

Mac / Linux:

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

Example requirements.txt

```
streamlit
pandas
scikit-learn
joblib
python-dotenv
google-genai
```

---

## 4️⃣ Add your Gemini API Key

Create a `.env` file in the root folder:

```
GEMINI_API_KEY=your_api_key_here
```

You can get a free key from:

https://ai.google.dev

---

# ▶️ Running the Application

Run the Streamlit app:

```
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

# 🧹 Text Preprocessing

Before prediction, the input text goes through preprocessing:

* Convert to lowercase
* Remove URLs
* Remove HTML tags
* Remove punctuation
* Remove numbers
* Remove unnecessary characters

This ensures the machine learning model receives **clean NLP input**.

---

# 📊 Model Prediction

The detection pipeline works as follows:

1. User inputs news text
2. Text is preprocessed
3. Converted into a Pandas Series
4. Passed into the trained ML model (`model.pkl`)
5. Model outputs:

   * Prediction (Real or Fake)
   * Confidence Score

---

# 📌 Example Workflow

1️⃣ Enter a **topic** → Generate a fake news article
2️⃣ Copy any article → Paste it into the detection section
3️⃣ Click **Check Authenticity**
4️⃣ View prediction and confidence score

---

# 🔒 Security Notes

* The Gemini API key is **not stored in the source code**.
* It is loaded from a `.env` file or entered temporarily in the UI.

---

# 👩‍💻 Author

**Yuvika Ajmera**

NLP & Generative AI Project

Built with ❤️ using Python, Machine Learning, and Generative AI.

---

# 🚀 Future Improvements

* Use **BERT or Transformer-based fake news detection**
* Add **model explanation (why prediction was made)**
* Add **news source credibility analysis**
* Deploy using **Streamlit Cloud**
* Add **multi-language support**

---
