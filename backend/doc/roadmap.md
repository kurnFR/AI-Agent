# Aegis AI-Agent Roadmap

This roadmap tracks the development milestones of the Aegis AI-Agent architecture.

---

## Completed Milestones

### v0.1 Foundation
- [x] Initial CEO architecture & Department routing
- [x] Specialized domain agents (Linux, FileSystem, Python, SQL)
- [x] PostgreSQL database manager & tool registry

### v0.2 Workflow & Execution Engine
- [x] Task lifecycle state transitions (`pending` -> `running` -> `completed` / `failed`)
- [x] Workflow DAG dependency validator and circular dependency detector
- [x] Partial failure resilience with independent task continuation
- [x] MariaDB & SQL Server database engine factory integration

### v0.3 Modernization & Productionization
- [x] FastAPI REST API service with OpenAPI specification
- [x] Centralized Department and Agent registries
- [x] Robust LLM JSON parsing service
- [x] Expanded FileSystem and hardened Shell/Python security tools
- [x] Full test suite refactor with hermetic pytest test cases
- [x] Comprehensive documentation (architecture, setup, conventions, changelog)

---

## Upcoming Milestones

### v0.4 Distributed Execution & Human-in-the-Loop
- [ ] Celery / Redis task queue for background asynchronous workflow execution
- [ ] Interactive human approval prompts for high-risk commands (e.g. database schema migrations)
- [ ] Agent conversation memory / stateful context persistence

### v0.5 Web UI & Observability
- [ ] Real-time React / Next.js dashboard for agent workflows
- [ ] OpenTelemetry distributed tracing and metrics
- [ ] Multi-model LLM provider routing (Anthropic, OpenAI, local Ollama)