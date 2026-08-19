# Changelog

All notable changes to the Aegis AI-Agent system are documented in this file.

---

## [v0.3.0] - 2026-08-19

### Added
- **FastAPI Web Layer**: Complete REST API interface in [`app/main.py`](file:///home/BIS/agy-test/AI-Agent/backend/app/main.py) and [`app/api/router.py`](file:///home/BIS/agy-test/AI-Agent/backend/app/api/router.py) with `/health`, `/api/v1/agent/execute`, and `/api/v1/workflows`.
- **Workflow DAG & Dependency Engine**: Directed Acyclic Graph validation, dependency tracking, task lifecycle transitions, and independent task continuation upon partial failures.
- **Robust JSON Parsing**: Regex-backed JSON extractor in [`app/services/json_parser.py`](file:///home/BIS/agy-test/AI-Agent/backend/app/services/json_parser.py) to reliably handle LLM responses with markdown ticks or conversational preambles.
- **Centralized Department & Agent Registries**: [`DepartmentRegistry`](file:///home/BIS/agy-test/AI-Agent/backend/app/departments/registry.py) and [`AgentRegistry`](file:///home/BIS/agy-test/AI-Agent/backend/app/agents/registry.py).
- **Multi-Database Support**: Connection factories for PostgreSQL, MariaDB, and SQL Server with pre-ping connection pooling.
- **FileSystem Tool Expansion**: Added `write`, `read`, `list`, `mkdir`, `delete`, and `exists` actions with safe path resolution.
- **Security & Command Sanitization**: Hardened [`CommandValidator`](file:///home/BIS/agy-test/AI-Agent/backend/app/security/command_validator.py) blocking destructive root manipulations, shutdown/reboot, shell fork-bombs, and unauthorized permissions modification.
- **Modern Hermetic Test Suite**: Refactored all 31 test modules in `backend/tests/` to standard pytest structure with deterministic mocks.

### Changed
- Refactored `BaseDepartment` to separate planning (`.plan()`) from execution (`.execute()`).
- Updated `ShellTool` and `PythonTool` to run with strict execution timeouts and sandboxed parameter handling.
- Configured dynamic environment loading via `python-dotenv` in [`app/config.py`](file:///home/BIS/agy-test/AI-Agent/backend/app/config.py).

---

## [v0.2.0] - 2026-08-11

### Added
- Workflow Result and Task Result models.
- Independent task continuation after dependency failures.
- Workflow runner type annotations and task dependency resolution.

---

## [v0.1.0] - 2026-08-07

### Added
- Initial CEO architecture and Department routers.
- Specialized agents (LinuxAgent, FileSystemAgent, PythonAgent, SQLAgent).
- PostgreSQL tool and database connection manager.
- Tool registry and execution engine.