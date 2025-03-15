# FinTech LLM End-to-End

A full-stack AI-powered FinTech system integrating real-time cryptocurrency market data, LLama-based financial analysis, personalized recommendations, fraud detection, and a simulated trading engine that uses a mock wallet with real market prices. This project includes three local LLama models (GGUF format) for:

- **Market Sentiment Analysis and Report Generation**
- **Personalized Financial Recommendations and Risk Profiling**
- **Customer Query Chat & Fraud Detection**

The web interface is built with Next.js and Tailwind CSS, while the backend uses FastAPI and integrates with Binance public API endpoints for genuine market data.

---

## Table of Contents

- [Features](#,#features)
- [Requirements](#,#requirements)
- [Tech Stack](#,#tech-stack)
  - [Backend](#,#backend)
  - [Frontend](#,#frontend)
- [Project Structure](#,#project-structure)
- [Installation and Running the Project](#,#installation-and-running-the-project)
- [LLama Models](#,#llama-models)
- [How It Works](#,#how-it-works)
- [License](#,#license)

---

## Features

- **Real-Time Market Data:**  
  Uses Binance’s public REST API (`/api/v3/ticker/price` and `/api/v3/klines`) to display genuine market prices and historical price trends.
  
- **Financial Report Generation:**  
  The sentiment analysis LLama model (GGUF) generates financial reports based on current market data.
  
- **Personalized Financial Recommendations:**  
  A dedicated LLama model provides risk profiling and customized trading advice.
  
- **Customer Query Chat:**  
  Interact with a real LLama model (GGUF) via chat. The model not only answers general queries but also detects potential fraudulent or suspicious market signals.
  
- **Simulated Trading Engine:**  
  Executes mock trades using real market data; the wallet is virtual so only developers know that the transactions are simulated.
  
- **Transaction Logging:**  
  All simulated trades are logged into a file and displayed on the dashboard.

---

## Requirements

- **Backend:**  
  - Python 3.8+  
  - Required Python packages (see `backend/requirements.txt`)  
  - [llama-cpp-python](https://pypi.org/project/llama-cpp-python/) (for LLama GGUF inference)  
  - Binance API (public endpoints are used; for authenticated endpoints, configure environment variables for API key and secret)

- **Frontend:**  
  - Node.js
  - npm
  - Next.js

---

## Tech Stack

### Backend

- **Language & Framework:** Python, FastAPI  
- **Web Server:** Uvicorn  
- **Model Inference:** llama-cpp-python (to load and run GGUF models)  
- **Data Source:** Binance REST API (and WebSocket if extended)  
- **Utilities:** Requests, Pandas, NumPy, XGBoost, TensorFlow (for backtesting simulation)

### Frontend

- **Framework:** Next.js  
- **Styling:** Tailwind CSS  
- **Charting:** Chart.js (via react-chartjs-2)  
- **JavaScript Library:** React

---

## Project Structure

```
fintech-llm/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── llm/
│   │   ├── sentiment.gguf
│   │   ├── recommendation.gguf
│   │   └── customer_query.gguf
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sentiment_model.py
│   │   ├── recommendation_model.py
│   │   ├── customer_query_model.py
│   │   ├── trade_agent.py
│   │   └── backtesting.py
│   └── utils/
│       ├── __init__.py
│       ├── binance_client.py
│       └── file_logging.py
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── postcss.config.js
    ├── tailwind.config.js
    ├── styles/
    │   └── globals.css
    ├── pages/
    │   ├── index.js
    │   ├── login.js
    │   └── dashboard.js
    └── components/
        ├── Header.js
        ├── MarketData.js
        ├── TradeDropdown.js
        ├── ChatBox.js
        └── TransactionLog.js
```

---

## Installation and Running the Project

### 1. Clone the Repository

Open a terminal (Powershell OR Linux Terminal) and clone the repository:

```
git clone https://github.com/aryann-anand/XNL-21BCE1596-LLM-1.git
cd fintech-llm
```

### 2. Setup and Run the Backend

1. **Navigate to the backend folder:**

   ```
   cd backend
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install required Python packages:**

   ```
   pip install -r requirements.txt
   ```

4. **Set Environment Variables (for using any authenticated endpoints in production):**

   ```
   set BINANCE_API_KEY=your_actual_api_key_here
   set BINANCE_API_SECRET=your_actual_api_secret_here
   ```

5. **Start the FastAPI server:**

   ```
   uvicorn app:app --reload
   ```

   The backend should now be accessible at [http://localhost:8000](http://localhost:8000).

### 3. Setup and Run the Frontend

1. **Open another terminal and navigate to the frontend folder:**

   ```
   cd ../frontend
   ```

2. **Install Node.js dependencies:**

   ```
   npm install
   ```

3. **Start the Next.js development server:**

   ```
   npm run dev
   ```

   The frontend should now be accessible at [http://localhost:3000](http://localhost:3000).

---

## LLaMA Models

The project uses three fine-tuned LLaMA GGUF models (from HuggingFace) placed in the `backend/llm/` folder:

1. **llama-2-13b-chat.Q4_K_M.gguf:**  
   Used by `sentiment_model.py` to generate a financial report based on market sentiment.

2. **llama-2-13b-chat.Q4_K_M-2.gguf:**  
   Used by `recommendation_model.py` to compute personalized financial recommendations and risk profiles based on the selected symbol (BTC-USDT or ETH-USDT).

3. **llama-2-7b-chat.Q4_K_M.gguf:**  
   Used by `customer_query_model.py` to answer any user queries. This model is loaded with the [llama-cpp-python](https://pypi.org/project/llama-cpp-python/) library and processes queries by combining user input with the current financial report context.

Each model is integrated via separate functions in the `models/` folder; during initialization, the file path is computed and the model is loaded for inference.

---

## How It Works

- **Backend:**  
  The FastAPI application provides multiple endpoints:
  - `/api/market-data`: Fetches live market ticker data from Binance.
  - `/api/generate-report`: Uses the sentiment LLama model to generate a financial report.
  - `/api/personalized-recommendation`: Uses the recommendation LLama model to offer personalized trading advice.
  - `/api/simulate-trade`: Simulates a trade using real-time market prices but a mock wallet.
  - `/api/transaction-logs`: Returns a log file of all mock transactions.
  - `/api/chat`: Processes customer queries using the customer query LLama model.
  - `/api/backtesting`: Implements simulated A/B testing with historical data for trade prediction.

- **Frontend:**  
  Built with Next.js and Tailwind CSS, the UI presents:
  - A login screen.
  - A dashboard displaying current market data and historical price trends (via Chart.js).
  - Dropdowns and input fields for executing simulated trades.
  - A live chat component to interact with the LLama-powered customer query model.
  - A list of transaction logs displaying details of simulated trades.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Submission: Aryan Anand  |  Reg No: 21BCE1596  |  LLM-Task 1 , XNL Innovations
