class CommandValidator:

    SAFE_COMMANDS = {
        "pwd",
        "ls",
        "whoami",
        "df",
        "free",
        "ps",
        "cat",
        "head",
        "tail",
        "find",
        "du"
    }

    BLOCKED_COMMANDS = {
        "rm",
        "reboot",
        "shutdown",
        "poweroff",
        "mkfs",
        "dd",
        "kill",
        "killall",
        "chmod",
        "chown",
        "sudo",
        "systemctl"
    }

    def validate(self, command: str):

        command = command.strip()

        if not command:
            return {
                "success": False,
                "error": "Empty command."
            }

        cmd = command.split()[0]

        if cmd in self.BLOCKED_COMMANDS:
            return {
                "success": False,
                "error": f"Blocked command: {cmd}"
            }

        if cmd not in self.SAFE_COMMANDS:
            return {
                "success": False,
                "error": f"Command not allowed: {cmd}"
            }

        return {
            "success": True,
            "error": None
        }