from app.orchestration.ceo import CEO
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


def test_ceo_registry():
    ceo = CEO(auto_register=False)
    ceo.register(DataDepartment())
    ceo.register(InfrastructureDepartment())
    ceo.register(SoftwareDepartment())

    depts = ceo.list_departments()
    assert "data" in depts
    assert "infrastructure" in depts
    assert "software" in depts

    assert ceo.get_department("data") is not None
    assert ceo.get_department("infrastructure") is not None
    assert ceo.get_department("software") is not None
    assert ceo.get_department("unknown") is None


if __name__ == "__main__":
    test_ceo_registry()
    print("test_ceo_registry: PASS")

