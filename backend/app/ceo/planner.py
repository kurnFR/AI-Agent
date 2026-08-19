from typing import Optional

from app.services.json_parser import extract_json
from app.services.llm_service import LLMService


class CEOPlanner:

    def __init__(self, llm: Optional[LLMService] = None):

        self.llm = llm or LLMService()

    def create_plan(self, message: str):

        prompt = f"""
You are the CEO of an AI company.

Your job is ONLY to choose the correct department.

Departments:

- infrastructure
    Linux
    Ubuntu
    Docker
    Shell
    Filesystem
    Disk
    Memory
    CPU
    Server

- data
    SQL
    PostgreSQL
    MySQL
    Database
    Query
    ETL

- software
    Python
    Programming
    Code
    Script

Return ONLY valid JSON.

Example 1

{{
    "department":"infrastructure",
    "reason":"Filesystem request"
}}

Example 2

{{
    "department":"data",
    "reason":"SQL request"
}}

Example 3

{{
    "department":"software",
    "reason":"Python request"
}}

User request:

{message}
"""

        try:
            response = self.llm.ask(prompt)
            plan = extract_json(response)
        except Exception:
            plan = {}

        if "department" not in plan or not plan["department"]:

            text = message.lower()

            if any(x in text for x in [
                "linux",
                "disk",
                "directory",
                "folder",
                "file",
                "filesystem",
                "shell",
                "docker",
                "pwd",
                "ls"
            ]):

                return {
                    "department": "infrastructure",
                    "reason": "Rule based fallback"
                }

            if any(x in text for x in [
                "select",
                "insert",
                "update",
                "delete",
                "sql",
                "postgres",
                "mysql",
                "database"
            ]):

                return {
                    "department": "data",
                    "reason": "Rule based fallback"
                }

            if any(x in text for x in [
                "python",
                "code",
                "script",
                "program"
            ]):

                return {
                    "department": "software",
                    "reason": "Rule based fallback"
                }

            return {
                "department": "software",
                "reason": "Default fallback"
            }

        return plan