from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.ceo.ceo import CEO
from app.execution.engine import ExecutionEngine
from app.execution.result import ExecutionResult
from app.execution.workflow import Workflow
from app.execution.workflow_result import WorkflowResult
from app.execution.workflow_runner import WorkflowRunner
from app.schemas.task_plan import TaskPlan
from app.tools.registry import ToolRegistry

router = APIRouter(prefix="/api/v1", tags=["Aegis Agent"])

# Singleton CEO and Tool instances for the API
tool_registry = ToolRegistry()
execution_engine = ExecutionEngine(tool_registry)
workflow_runner = WorkflowRunner(execution_engine)
ceo_instance = CEO()


class MessageRequest(BaseModel):
    message: str = Field(..., description="User prompt or instruction for the AI Agent system")


class ExecutePlanRequest(BaseModel):
    plan: TaskPlan


class WorkflowExecuteRequest(BaseModel):
    workflow: Workflow
    plans: List[TaskPlan]


@router.get("/health", status_code=status.HTTP_200_OK)
def api_health() -> Dict[str, str]:
    return {"status": "ok", "service": "Aegis AI Agent"}


@router.get("/tools", status_code=status.HTTP_200_OK)
def list_tools() -> Dict[str, List[str]]:
    return {"tools": tool_registry.names()}


@router.get("/departments", status_code=status.HTTP_200_OK)
def list_departments() -> Dict[str, Any]:
    departments_info = {}
    for name in ceo_instance.department_names():
        dep = ceo_instance.get_department(name)
        departments_info[name] = {
            "name": name,
            "agents": dep.agents() if dep else []
        }
    return {"departments": departments_info}


@router.post("/agent/execute", response_model=ExecutionResult, status_code=status.HTTP_200_OK)
def execute_message(request: MessageRequest):
    try:
        result = ceo_instance.execute(request.message)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(ex)}"
        )


@router.post("/tools/execute", response_model=ExecutionResult, status_code=status.HTTP_200_OK)
def execute_plan_directly(request: ExecutePlanRequest):
    try:
        return execution_engine.execute(request.plan)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Direct plan execution failed: {str(ex)}"
        )


@router.post("/workflows/execute", response_model=WorkflowResult, status_code=status.HTTP_200_OK)
def execute_workflow(request: WorkflowExecuteRequest):
    try:
        result = workflow_runner.execute(request.workflow, request.plans)
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(ex)}"
        )
