from app.planning.ceo import CEOPlanner
from app.planning.department import DepartmentPlanner


ceo = CEOPlanner()

print("=" * 60)
print(ceo.create_plan("show disk usage"))

print("=" * 60)

data = DepartmentPlanner(
    department="Data",
    agents=[
        "sql",
        "bi",
        "chat"
    ]
)

print(data.create_plan("SELECT * FROM customer"))
