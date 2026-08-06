from backend.app.tools.shell.tool import ShellTool

tool = ShellTool()

tests = [
    "pwd",
    "whoami",
    "ls",
    "rm -rf /",
    "shutdown now",
    "sudo reboot",
]

for command in tests:

    print("=" * 60)
    print(command)
    print(tool.run(command))
