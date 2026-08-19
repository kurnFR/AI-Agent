# Aegis AI-Agent Conventions

This document outlines the design standards, architectural guidelines, and coding practices followed across the Aegis codebase.

---

## 1. Architectural Layers & Separation of Concerns

Aegis enforces strict unidirectional communication across layers:

```
[FastAPI / Web API] ──► [CEO / Orchestration] ──► [Department] ──► [Agent] ──► [ExecutionEngine] ──► [Tools]
```

- **API Layer (`app/api/`, `app/main.py`)**: Handles HTTP requests, validation, serializing Pydantic models, and lifespan events. Must not execute shell or database logic directly.
- **CEO Layer (`app/ceo/`, `app/orchestration/`)**: High-level routing and strategy across departments.
- **Department Layer (`app/departments/`)**: Domain orchestration (Infrastructure, Data, Software). Responsible for planning task decomposition and delegating to specialized agents.
- **Agent Layer (`app/agents/`)**: Specialized prompt formatting, LLM querying, and JSON parsing into structured `TaskPlan` objects.
- **Execution Layer (`app/execution/`)**: Task lifecycle management, dependency resolution (DAG), workflow execution, and error containment.
- **Tool Layer (`app/tools/`)**: Sandboxed, deterministic system interactions (PostgreSQL, MariaDB, SQL Server, FileSystem, Shell, Python).

---

## 2. Coding Standards

### Python & Typing
- Target Python version: `>= 3.10` (recommended Python 3.12).
- Type annotations are required on all public methods and functions.
- All domain payloads and return structures must use `pydantic.BaseModel` models.

### Planning vs Execution Segregation
- Agents and Planners produce **`TaskPlan`** objects via `.plan(message)`.
- Tools and Engines consume **`TaskPlan`** and produce **`ExecutionResult`** or **`WorkflowResult`** via `.execute(plan)`.
- Tools must never invoke LLMs directly. Agents must never execute system actions without going through the `ExecutionEngine`.

### Security & Sanitization
- All shell executions must pass through [`CommandValidator`](file:///home/BIS/agy-test/AI-Agent/backend/app/security/command_validator.py).
- Unsafe commands (`rm -rf /`, `shutdown`, `reboot`, fork bombs) are blocked unconditionally.
- Commands are executed via tokenized parameter lists (`shell=False`) with strict timeouts (`EXECUTION_TIMEOUT`).
- Filesystem operations are strictly bound within `WORKSPACE_ROOT` unless explicitly configured.

---

## 3. Error Handling Guidelines

- Execution tools must never throw uncaught exceptions during normal workflow runs; they must catch exceptions and return `ExecutionResult(success=False, error=str(ex))`.
- LLM parsing failures must fall back to structured, safe fallback plans with informative error reasons rather than crashing.
- Failed tasks in a workflow mark dependent tasks as skipped without executing them, while independent tasks continue.

---

## 4. Testing Conventions

- Test files must reside in `backend/tests/` with the `test_*.py` naming convention.
- Unit tests must be hermetic and not require external network or live LLM/Ollama services (use mock LLMs and in-memory SQLite for database testing).
- Each test file must contain clear `assert` statements and a callable `test_*()` function with `if __name__ == "__main__":` entrypoints.
