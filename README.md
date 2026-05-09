# Legal AI Detector

An AI-powered system that analyzes legal documents and detects inconsistencies, risky clauses, contradictions, and missing information using NLP and Machine Learning techniques.

---

# 📌 Features

* 📄 Upload legal PDF documents
* 🔍 Extract text using PyMuPDF
* 🤖 AI-powered legal analysis
* ⚠️ Detect inconsistencies and risky clauses
* 📊 Generate detailed reports
* 🌐 Responsive web interface

---

# 🛠️ Technologies Used

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python
* FastAPI
* Uvicorn

## AI / NLP

* Google Gemini API
* NLP Techniques

## Libraries

* PyMuPDF (`fitz`)
* JSON

---

# 📂 Project Structure

```bash id="c3y4h4"
Legal-AI-Detector/
│
├── frontend/
│   └── index.html
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── detector.py
│   ├── extractor.py
|   └── analyzer.py
│   └── segmentor.py
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash id="gz79fr"
git clone https://github.com/your-username/legal-ai-detector.git
cd legal-ai-detector
```

## 2️⃣ Install Dependencies

```bash id="js1v0y"
pip install -r backend/requirements.txt
```

## 3️⃣ Run Backend Server

```bash id="7fajee"
uvicorn backend.app:app --reload
```

## 4️⃣ Open Frontend

Open `frontend/index.html` in your browser.

---

# 🚀 How It Works

1. Upload a legal PDF document
2. System extracts document text
3. AI analyzes clauses and risks
4. Displays inconsistencies and findings
5. Generates final report

---

# 🎯 Future Scope

* Multi-language support
* Advanced legal clause classification
* AI chatbot integration
* Cloud deployment
* Real-time collaboration

---

# 👩‍💻 Authors

* Shreya KS
* Akshatha HR
* Harshitha L

---

# 📜 License

This project is developed for educational and academic purposes.
