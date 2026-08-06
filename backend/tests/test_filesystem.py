from backend.app.tools.filesystem.tool import FileSystemTool

fs = FileSystemTool()

print(fs.list("/app"))
