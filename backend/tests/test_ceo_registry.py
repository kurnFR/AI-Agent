from app.orchestration.ceo import CEO

from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


ceo = CEO()

ceo.register(DataDepartment())
ceo.register(InfrastructureDepartment())
ceo.register(SoftwareDepartment())

print("=" * 60)

print(ceo.list_departments())

print("=" * 60)

print(ceo.get_department("data"))

print("=" * 60)

print(ceo.get_department("infrastructure"))

print("=" * 60)

print(ceo.get_department("software"))
