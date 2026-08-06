class CommandValidator:

    SAFE_COMMANDS = {
        "pwd",
        "ls",
        "df",
        "du",
        "whoami",
        "free",
        "ps",
        "cat",
        "head",
        "tail",
        "find"
    }

    BLOCKED_COMMANDS = {
        "rm",
        "mv",
        "cp",
        "chmod",
        "chown",
        "reboot",
        "shutdown",
        "poweroff",
        "mkfs",
        "dd",
        "kill",
        "killall",
        "sudo",
        "systemctl"
    }

    def validate(self, command: str):

        if not command:
            return False

        command = command.strip()

        if not command:
            return False

        cmd = command.split()[0]

        if cmd in self.BLOCKED_COMMANDS:
            return False

        if cmd not in self.SAFE_COMMANDS:
            return False

        return True
