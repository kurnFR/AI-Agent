from typing import Dict, List, Optional

from app.ceo.planner import CEOPlanner
from app.departments.base.department import BaseDepartment
from app.departments.data.department import DataDepartment
from app.departments.infrastructure.department import InfrastructureDepartment
from app.departments.software.department import SoftwareDepartment
from app.execution.result import ExecutionResult


class CEO:

    def __init__(self, auto_register: bool = True):

        self.departments: Dict[str, BaseDepartment] = {}
        self.planner = CEOPlanner()

        if auto_register:
            self.register(InfrastructureDepartment())
            self.register(DataDepartment())
            self.register(SoftwareDepartment())

    def register(self, department: BaseDepartment):

        self.departments[department.name] = department

    def get_department(self, name: str) -> Optional[BaseDepartment]:

        return self.departments.get(name)

    def department_names(self) -> List[str]:

        return sorted(list(self.departments.keys()))

    def list_departments(self) -> List[str]:

        return self.department_names()

    def list(self) -> List[str]:

        return self.department_names()

    def execute(self, message: str) -> ExecutionResult:

        department_plan = self.planner.create_plan(message)

        dep_name = department_plan.get("department", "software") if isinstance(department_plan, dict) else "software"
        department = self.get_department(dep_name)

        if department is None:

            return ExecutionResult(
                success=False,
                tool="ceo",
                output=None,
                error=f"Department '{dep_name}' not found."
            )

        return department.plan(message)