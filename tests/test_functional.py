import pytest

from unittest.mock import patch
from src.manager import Manager
from src.models import Parameters, Tenant, Apartment, Transfer
from src.models import Bill


def test_total_due_pln():
    parameters = Parameters()
    manager = Manager(parameters)
    
    rozliczenie = manager.get_settlement("apart-polanka", 2025, 1)
    
    assert rozliczenie is not None, "Brak danych rozliczeniowych dla podanego miesiąca i mieszkania"
    
    spr = manager.create_tenants_settlements(rozliczenie)
    suma_najemcow = sum(lokator.total_due_pln for lokator in spr)
    
    assert suma_najemcow == rozliczenie.total_due_pln

def test_debtors_returns_tenants_with_insufficient_transfers():
    with patch.object(Manager, 'load_data'):
        manager = Manager(Parameters())
        
        from src.models import Tenant, Transfer, Apartment
        manager.apartments = {"apart-1": Apartment(key="apart-1", name="Test", location="Test", area_m2=50.0, rooms={})}
        manager.tenants = {"tenant-1": Tenant(name="Adam Kowalski", apartment="apart-1", room="room-1", rent_pln=1500.0, deposit_pln=0.0, date_agreement_from="2025-01-01", date_agreement_to="2025-12-31")}
        manager.transfers = [Transfer(amount_pln=1000.0, date="2025-01-05", settlement_year=2025, settlement_month=1, tenant="Adam Kowalski")]
        
        debtors = manager.get_debtors('apart-1', 2025, 1)
        
        assert len(debtors) == 1
        assert debtors[0]["tenant"] == "Adam Kowalski"
        assert debtors[0]["debt"] == 500.0

def test_annual_report_totals():
    with patch.object(Manager, 'load_data'):
        manager = Manager(Parameters())
        from src.models import Transfer, Bill
        
        manager.transfers = [Transfer(amount_pln=3000.0, date="2025-01-05", settlement_year=2025, settlement_month=1, tenant="Test")]
        manager.bills = [Bill(amount_pln=1000.0, date_due="2025-01-15", apartment="apart-1", settlement_year=2025, settlement_month=1, type="rent")]
        
        report = manager.get_annual_report(2025)
        
        assert report["year"] == 2025
        assert report["total_costs"] == 1000.0
        assert report["total_income"] == 3000.0
        assert report["net_balance"] == 2000.0
        assert report["by_month"][1]["balance"] == 2000.0