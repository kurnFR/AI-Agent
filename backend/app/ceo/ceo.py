from app.ceo.planner import CEOPlanner
from app.execution.result import ExecutionResult


class CEO:

    def __init__(self):

        self.departments = {}

        self.planner = CEOPlanner()

    def register(self, department):

        self.departments[
            department.name
        ] = department

    def get_department(self, name):

        return self.departments.get(name)

    def department_names(self):

        return list(
            self.departments.keys()
        )

    def execute(self, message):

        department_plan = self.planner.create_plan(message)

        print("=" * 60)
        print("CEO PLAN")
        print(department_plan)
        print(type(department_plan))
        print("=" * 60)

        department = self.get_department(
            department_plan["department"]
        )

        if department is None:

            return ExecutionResult(
                success=False,
                tool="ceo",
                output=None,
                error=f"Department '{department_plan['department']}' not found."
            )

        return department.plan(message)