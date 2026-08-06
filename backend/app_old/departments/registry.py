class DepartmentRegistry:

    def __init__(self):
        self.departments = {}

    def register(self, department):
        self.departments[department.name] = department

    def unregister(self, name):
        self.departments.pop(name, None)

    def get(self, name):
        return self.departments.get(name)

    def exists(self, name):
        return name in self.departments

    def list(self):
        return list(self.departments.values())

    def names(self):
        return list(self.departments.keys())
