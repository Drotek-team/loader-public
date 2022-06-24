import pytest

from .....family_manager.family_manager import FamilyManager
from .....procedure.show_check.family_manager_check.family_manager_check_procedure import (
    apply_family_check_procedure,
)
from .....procedure.show_check.family_manager_check.family_manager_check_report import (
    FamilyManagerCheckReport,
)


@pytest.fixture
def valid_family_manager():
    return FamilyManager()


def test_valid_family_manager(valid_family_manager: FamilyManager):
    family_manager_check_report = 0
    apply_family_check_procedure(valid_family_manager)
