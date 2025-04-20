from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Invoice(BaseModel):
    number: Optional[str] = None  # Numer faktury
    client_name: Optional[str] = None  # Nazwa klienta
    seller_name: Optional[str] = None  # Nazwa sprzedawcy
    tax_number: Optional[str] = None  # NIP
    total_net_amount: float  # Kwota netto
    total_tax_amount: float  # Kwota VAT
    amount: float  # Kwota brutto
    currency: Optional[str] = "PLN"
    issue_date: Optional[date] = None  # Data wystawienia
    due_date: Optional[date] = None  # Termin płatności


class Transaction(BaseModel):
    sender_name: Optional[str] = None  # Nadawca przelewu
    amount: float
    currency: Optional[str] = "PLN"
    transfer_date: Optional[date] = None
    description: Optional[str] = None  # Tytuł przelewu


class MatchRequest(BaseModel):
    invoices: List[Invoice]
    transactions: List[Transaction]