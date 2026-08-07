from app.ceo.ceo import CEO

from app.tools.registry import ToolRegistry

from app.tools.shell.tool import ShellTool
from app.tools.filesystem.tool import FileSystemTool
from app.tools.python.tool import PythonTool

from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.data.department import DataDepartment
from app.departments.software.department import SoftwareDepartment

from app.agents.linux.agent import LinuxAgent
from app.agents.filesystem.agent import FileSystemAgent
from app.agents.sql.agent import SQLAgent
from app.agents.python.agent import PythonAgent


registry = ToolRegistry()

registry.register(ShellTool())
registry.register(FileSystemTool())
registry.register(PythonTool())


infra = InfrastructureDepartment(registry)

infra.register(LinuxAgent())
infra.register(FileSystemAgent())


data = DataDepartment(registry)

data.register(SQLAgent())


software = SoftwareDepartment(registry)

software.register(PythonAgent())


ceo = CEO()

ceo.register(infra)
ceo.register(data)
ceo.register(software)


tests = [

    "show current directory",

    "list files",

    "write hello world in python",

    "select * from customer"

]


for t in tests:

    print("=" * 60)

    print("USER :", t)

    result = ceo.execute(t)

    print(result)
