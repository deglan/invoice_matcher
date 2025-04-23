import joblib
import pandas as pd

from ml.extract import extract_features

model = joblib.load('ml/model.pkl')

FEATURE_NAMES = [
    "amount_diff",
    "net_diff",
    "tax_ratio",
    "days_diff",
    "days_to_due",
    "similarity_name",
    "similarity_desc"
]

async def predict_match(invoice, transaction):
    values = extract_features(invoice, transaction)
    input_df = pd.DataFrame([values], columns=FEATURE_NAMES)

    print("🧠 FEATURES SENT TO MODEL:", input_df.to_dict(orient="records")[0])

    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)
    return int(prediction[0]), float(probability[0][1])