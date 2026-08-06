from app.departments.registry import DepartmentRegistry

from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


registry = DepartmentRegistry()

registry.register(DataDepartment())
registry.register(InfrastructureDepartment())
registry.register(SoftwareDepartment())

print(registry.names())

print(registry.get("data"))

print(registry.get("infrastructure"))

print(registry.get("software"))
