from app.ceo.ceo import CEO
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


def test_ceo_registration():
    ceo = CEO(auto_register=False)
    ceo.register(DataDepartment())
    ceo.register(InfrastructureDepartment())
    ceo.register(SoftwareDepartment())

    names = ceo.department_names()
    assert "data" in names
    assert "infrastructure" in names
    assert "software" in names
    assert len(names) == 3


if __name__ == "__main__":
    test_ceo_registration()
    print("test_ceo: PASS")

