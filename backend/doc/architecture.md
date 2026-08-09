 CEO
                      │
                      ▼
               CEO Planner
                      │
                      ▼
             Department Router
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
Infrastructure      Data        Software
        │             │              │
        ▼             ▼              ▼
 Linux/File      SQLAgent      PythonAgent
        │             │              │
        ▼             ▼              ▼
      TaskPlan      TaskPlan      TaskPlan
              │
              ▼
        ExecutionEngine
              │
              ▼
        Tool Registry
              │
      ┌───────┼──────────┐
      ▼       ▼          ▼
 Filesystem  Shell     Python