# Smart Matcher

Smart Matcher is a microservice designed to **match business invoices with bank transactions** using machine learning and string similarity techniques.

## 🚀 Features

- Collects invoices and transactions in MongoDB
- Matches transactions to invoices using ML model
- Exposes:
  - REST API: for basic interaction
  - gRPC API: for prediction via ML model

---

## 📦 Installation

You can run the service either locally or using Docker.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/invoice_matcher.git
cd invoice_matcher
```

### 2. Create `.env` file

Create a `.env` file or export the following environment variables:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=invoice_matcher
MONGO_INVOICE_COLLECTION=invoices
MONGO_TRANSACTION_COLLECTION=transactions
```

### 3. Install dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the service

```bash
make run
```

> This will start both the REST and gRPC servers.

---

## 🧐 Model

The machine learning model used is a **Random Forest Classifier** trained on feature vectors that include:

- Amount difference
- Date difference
- Tax ratio
- Cosine similarity of names and descriptions

---

