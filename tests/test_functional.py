import pytest

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
