from app.departments.registry import DepartmentRegistry

from app.planning.ceo import CEOPlanner


class CEO:

    def __init__(self):

        self.registry = DepartmentRegistry()
        self.planner = CEOPlanner()

    def register(self, department):

        self.registry.register(department)

    def execute(self, message: str):

        plan = self.planner.create_plan(message)

        department = self.registry.get(plan["department"])

        if department is None:
            return {
                "success": False,
                "error": f"Department '{plan['department']}' not found."
            }

        return department.execute(message)
