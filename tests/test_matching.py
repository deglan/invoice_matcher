import pytest
import asyncio
from service.matcher_service import get_match  
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_match_returns_best_invoice():
    # 🔧 Dane testowe
    transaction = {
        "sender_name": "Jan Kowalski",
        "amount": 1234.56,
        "currency": "PLN",
        "transfer_date": "2024-04-05",
        "description": "FV/2024/04/001"
    }

    fake_invoice_1 = {
        "number": "FV/2024/04/001",
        "client_name": "Jan Kowalski",
        "seller_name": "Firma ABC",
        "tax_number": "1234567890",
        "total_net_amount": 1000.00,
        "total_tax_amount": 234.56,
        "amount": 1234.56,
        "currency": "PLN",
        "issue_date": "2024-04-01",
        "due_date": "2024-04-15"
    }

    fake_invoice_2 = {
        "number": "FV/2024/04/002",
        "client_name": "Anna Nowak",
        "seller_name": "Firma XYZ",
        "tax_number": "9876543210",
        "total_net_amount": 800.00,
        "total_tax_amount": 184.00,
        "amount": 984.00,
        "currency": "PLN",
        "issue_date": "2024-04-02",
        "due_date": "2024-04-16"
    }

    with patch("app.matcher.predict_match", new_callable=AsyncMock) as mock_predict, \
         patch("app.matcher.get_all_invoices", new_callable=AsyncMock) as mock_get_invoices:
        
        mock_predict.side_effect = [
            (1, 0.95),  # invoice_1
            (0, 0.3)    # invoice_2
        ]
        mock_get_invoices.return_value = [fake_invoice_1, fake_invoice_2]

        result = await get_match(transaction)

        assert result["invoice"]["number"] == "FV/2024/04/001"
        assert result["prediction"] == 1
        assert result["probability"] == 0.95
