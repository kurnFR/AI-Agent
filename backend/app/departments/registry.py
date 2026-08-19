from typing import Dict, List, Optional
from app.departments.base.department import BaseDepartment


class DepartmentRegistry:

    def __init__(self):

        self._departments: Dict[str, BaseDepartment] = {}

    def register(self, department: BaseDepartment) -> None:

        self._departments[department.name] = department

    def get(self, name: str) -> Optional[BaseDepartment]:

        return self._departments.get(name)

    def names(self) -> List[str]:

        return sorted(self._departments.keys())

    def list(self) -> List[BaseDepartment]:

        return list(self._departments.values())
