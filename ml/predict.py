import joblib

from ml.extract import extract_features

model = joblib.load('ml/model.pkl')

async def predict_match(invoice, transaction):
    """
    Predict if an invoice matches a transaction using the trained model.
    """
    features = extract_features(invoice, transaction)
    prediction = model.predict([features])
    probability = model.predict_proba([features])
    return int(prediction[0]), float(probability[0][1])