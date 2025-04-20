from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def safe_str(value):
    return str(value) if value is not None else ""

def extract_features(invoice, transaction):
    amount_diff = abs(invoice["amount"] - transaction["amount"])
    net_diff = abs(invoice["total_net_amount"] - transaction["amount"])
    tax_ratio = (
        invoice["total_tax_amount"] / invoice["total_net_amount"]
        if invoice["total_net_amount"] else 0.0
    )

    issue_date = invoice.get("issue_date")
    due_date = invoice.get("due_date")
    transfer_date = transaction.get("transfer_date")

    if isinstance(issue_date, str):
        issue_date = datetime.fromisoformat(issue_date)
    if isinstance(due_date, str):
        due_date = datetime.fromisoformat(due_date)
    if isinstance(transfer_date, str):
        transfer_date = datetime.fromisoformat(transfer_date)

    days_diff = abs((transfer_date - issue_date).days) if issue_date and transfer_date else 999
    days_to_due = (transfer_date - due_date).days if due_date and transfer_date else 999

    # Zabezpieczenia przed None
    client = safe_str(invoice.get("client_name"))
    sender = safe_str(transaction.get("sender_name"))
    desc = safe_str(transaction.get("description"))
    number = safe_str(invoice.get("number"))

    tfidf = TfidfVectorizer().fit([client, sender, desc, number])
    vectors = tfidf.transform([client, sender, desc, number]).toarray()

    similarity_name = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    similarity_desc = cosine_similarity([vectors[2]], [vectors[3]])[0][0]

    return [
        amount_diff,
        net_diff,
        tax_ratio,
        days_diff,
        days_to_due,
        similarity_name,
        similarity_desc,
    ]