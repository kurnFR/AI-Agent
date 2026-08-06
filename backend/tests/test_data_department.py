from app.departments.data.department import DataDepartment

from app.agents.sql.agent import SQLAgent


department = DataDepartment()

department.register(SQLAgent(None))


tests = [
    "SELECT * FROM customer",
    "SELECT COUNT(*) FROM sales"
]


for t in tests:

    print("=" * 60)
    print(t)
    print(department.execute("sql", t))