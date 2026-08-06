from app.planning.ceo import CEOPlanner


planner = CEOPlanner()

tests = [
    "show disk usage",
    "list /app",
    "SELECT * FROM customer",
    "write python hello world",
    "who are you"
]

for message in tests:

    print("=" * 60)
    print(message)

    plan = planner.create_plan(message)

    print(plan)