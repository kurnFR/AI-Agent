from app.departments.registry import DepartmentRegistry
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


def test_department_registry():
    registry = DepartmentRegistry()

    registry.register(DataDepartment())
    registry.register(InfrastructureDepartment())
    registry.register(SoftwareDepartment())

    names = registry.names()
    assert "data" in names
    assert "infrastructure" in names
    assert "software" in names

    assert registry.get("data") is not None
    assert registry.get("infrastructure") is not None
    assert registry.get("software") is not None
    assert registry.get("unknown") is None
    assert len(registry.list()) == 3


if __name__ == "__main__":
    test_department_registry()
    print("test_department_registry: PASS")

