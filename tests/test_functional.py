import pytest

from src.manager import Manager
from src.models import Parameters, Tenant, Apartment, Transfer
from src.models import Bill


def test_total_due_pln():
    parameters = Parameters()
    manager = Manager(parameters)
    rozliczenie = manager.get_settlement("apart-polanka", 2025, 1)
    print(rozliczenie)
    spr = manager.create_tenants_settlements(rozliczenie)
    
