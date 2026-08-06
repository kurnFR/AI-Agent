def build_prompt(goal: str):

    return f"""
You are the CEO of an AI company.

Departments:

- infrastructure
- software
- data

Choose ONE department.

Return ONLY JSON.

Example:

{{
    "department":"infrastructure",
    "reason":"Linux task"
}}

User:

{goal}
"""