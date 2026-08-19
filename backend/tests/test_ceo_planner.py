from app.planning.ceo import CEOPlanner


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "disk" in prompt:
            return '{"department":"infrastructure", "reason":"disk request"}'
        elif "SELECT" in prompt:
            return '{"department":"data", "reason":"sql query"}'
        return '{"department":"software", "reason":"python task"}'


def test_ceo_planner():
    mock_llm = MockLLM()
    planner = CEOPlanner(llm=mock_llm)

    infra_plan = planner.create_plan("show disk usage")
    assert infra_plan["department"] == "infrastructure"

    data_plan = planner.create_plan("SELECT * FROM customer")
    assert data_plan["department"] == "data"

    soft_plan = planner.create_plan("write python hello world")
    assert soft_plan["department"] == "software"


if __name__ == "__main__":
    test_ceo_planner()
    print("test_ceo_planner: PASS")