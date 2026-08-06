from app.ceo.ceo import CEO

from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment


ceo = CEO()

ceo.register(DataDepartment())
ceo.register(InfrastructureDepartment())
ceo.register(SoftwareDepartment())

print(ceo.departments.list())
