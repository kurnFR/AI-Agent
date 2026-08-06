from app.departments.data.department import DataDepartment

from app.agents.sql.agent import SQLAgent


department = DataDepartment()

department.register(
    SQLAgent()
)

tests = [
    "SELECT * FROM customer",
    "SELECT COUNT(*) FROM sales"
]

for t in tests:

    print("=" * 60)
    print(t)

    result = department.execute(t)

    print(result)