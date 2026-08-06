from app.departments.data.planner import DataPlanner


planner = DataPlanner()

tests = [
    "SELECT * FROM customer",
    "SELECT COUNT(*) FROM sales"
]

for t in tests:

    print("=" * 60)

    print(t)

    print(planner.create_plan(t))
