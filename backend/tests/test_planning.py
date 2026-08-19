from app.planning.ceo import CEOPlanner
from app.planning.department import DepartmentPlanner


class MockLLM:
    def ask(self, prompt: str) -> str:
        if "CEO" in prompt or "department" in prompt.lower():
            return '{"department":"Infrastructure"}'
        elif "agent" in prompt.lower():
            return '{"agent":"sql"}'
        return '{"plan":"ok"}'


def test_planning():
    mock_llm = MockLLM()
    ceo = CEOPlanner(llm=mock_llm)
    res_ceo = ceo.create_plan("show disk usage")
    assert res_ceo.get("department") == "Infrastructure"

    data = DepartmentPlanner(
        department="Data",
        agents=["sql", "bi", "chat"],
        llm=mock_llm
    )
    res_data = data.create_plan("SELECT * FROM customer")
    assert res_data.get("agent") == "sql"


if __name__ == "__main__":
    test_planning()
    print("test_planning: PASS")

