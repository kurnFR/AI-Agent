from app.departments.data.planner import DataPlanner


class MockLLM:
    def ask(self, prompt: str) -> str:
        return '{"agent":"sql"}'


def test_data_planner():
    planner = DataPlanner(llm=MockLLM())

    plan = planner.create_plan("SELECT * FROM customer")
    assert plan["agent"] == "sql"

    plan2 = planner.create_plan("SELECT COUNT(*) FROM sales")
    assert plan2["agent"] == "sql"


if __name__ == "__main__":
    test_data_planner()
    print("test_data_planner: PASS")

