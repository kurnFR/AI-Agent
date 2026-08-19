import tempfile
from pathlib import Path

from app.schemas.task_plan import TaskPlan
from app.tools.filesystem.tool import FileSystemTool


def test_filesystem_tool():
    with tempfile.TemporaryDirectory() as tmpdir:
        fs = FileSystemTool(workspace_root=tmpdir)

        # 1. Write file
        test_file = Path(tmpdir) / "test.txt"
        res_write = fs.execute(TaskPlan(
            tool="filesystem",
            action="write",
            target=str(test_file),
            payload={"content": "hello filesystem"}
        ))
        assert res_write.success is True
        assert test_file.exists()
        assert test_file.read_text() == "hello filesystem"

        # 2. Read file
        res_read = fs.execute(TaskPlan(
            tool="filesystem",
            action="read",
            target=str(test_file)
        ))
        assert res_read.success is True
        assert res_read.output == "hello filesystem"

        # 3. Exists check
        res_exists = fs.execute(TaskPlan(
            tool="filesystem",
            action="exists",
            target=str(test_file)
        ))
        assert res_exists.success is True
        assert res_exists.output is True

        # 4. Make directory
        sub_dir = Path(tmpdir) / "subdir"
        res_mkdir = fs.execute(TaskPlan(
            tool="filesystem",
            action="mkdir",
            target=str(sub_dir)
        ))
        assert res_mkdir.success is True
        assert sub_dir.is_dir()

        # 5. List directory
        res_list = fs.execute(TaskPlan(
            tool="filesystem",
            action="list",
            target=tmpdir
        ))
        assert res_list.success is True
        assert "test.txt" in res_list.output
        assert "subdir" in res_list.output

        # 6. Delete file
        res_del = fs.execute(TaskPlan(
            tool="filesystem",
            action="delete",
            target=str(test_file)
        ))
        assert res_del.success is True
        assert not test_file.exists()

        # 7. Delete nonexistent file
        res_del_none = fs.execute(TaskPlan(
            tool="filesystem",
            action="delete",
            target=str(test_file)
        ))
        assert res_del_none.success is False


if __name__ == "__main__":
    test_filesystem_tool()
    print("test_filesystem_tool: PASS")

