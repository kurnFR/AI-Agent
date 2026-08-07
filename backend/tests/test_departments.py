from app.agents.linux.agent import LinuxAgent
from app.agents.filesystem.agent import FileSystemAgent
from app.agents.sql.agent import SQLAgent

from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.data.department import DataDepartment


infra = InfrastructureDepartment()

infra.register(LinuxAgent())
infra.register(FileSystemAgent())

print("=" * 60)
print(infra.plan("show disk usage"))

print("=" * 60)

data = DataDepartment()

data.register(SQLAgent())

print(data.plan("SELECT * FROM customer"))
