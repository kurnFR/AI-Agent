from app.schemas.task_plan import TaskPlan
from app.security.command_validator import CommandValidator
from app.tools.shell.tool import ShellTool


def test_command_validator():
    validator = CommandValidator()

    # Allowed safe commands
    safe_commands = ["pwd", "whoami", "ls", "ls -la", "cat test.txt"]
    for cmd in safe_commands:
        assert validator.validate(cmd) is True, f"Expected {cmd} to be valid"

    # Blocked dangerous commands
    dangerous_commands = [
        "rm -rf /",
        "rm -rf /etc",
        "shutdown now",
        "sudo reboot",
        "chmod 777 /etc/passwd",
        "mkfs.ext4 /dev/sda",
        ":(){ :|:& };:"
    ]
    for cmd in dangerous_commands:
        assert validator.validate(cmd) is False, f"Expected {cmd} to be blocked"


def test_shell_tool_security():
    tool = ShellTool()

    # Blocked execution via shell tool
    res_blocked = tool.execute(TaskPlan(
        tool="shell",
        action="execute",
        target="rm -rf /",
        payload={}
    ))
    assert res_blocked.success is False
    assert "blocked or unsafe" in res_blocked.error

    # Allowed execution
    res_safe = tool.execute(TaskPlan(
        tool="shell",
        action="execute",
        target="pwd",
        payload={}
    ))
    assert res_safe.success is True
    assert res_safe.output["code"] == 0


if __name__ == "__main__":
    test_command_validator()
    test_shell_tool_security()
    print("test_security: PASS")

