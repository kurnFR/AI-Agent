import shlex


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
        "find",
        "echo",
        "date",
        "uptime",
        "uname"
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
        "su",
        "systemctl",
        "nc",
        "netcat",
        "curl",
        "wget",
        "bash",
        "sh",
        "zsh"
    }

    DANGEROUS_OPERATORS = {";", "&", "|", "`", "$", "(", ")", ">", "<"}

    def validate(self, command: str) -> bool:

        if not command or not isinstance(command, str):
            return False

        command = command.strip()
        if not command:
            return False

        # Reject dangerous shell chaining/substitution characters
        if any(op in command for op in self.DANGEROUS_OPERATORS):
            return False

        try:
            tokens = shlex.split(command)
        except Exception:
            return False

        if not tokens:
            return False

        cmd = tokens[0].strip()

        if cmd in self.BLOCKED_COMMANDS:
            return False

        if cmd not in self.SAFE_COMMANDS:
            return False

        return True

