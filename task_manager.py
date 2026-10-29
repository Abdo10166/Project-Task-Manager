import json
import os
import time

MSG_INVALID_NUMBER = "Please enter a valid number!"
MSG_NO_TASKS = "You don't have any Tasks :)"
MSG_TASK_NOT_FOUND = "Wrong: task not found"


class Controller:
    def __init__(self, data=None):
        self.data = data if data is not None else []

    def print_tasks(self):
        """Print all tasks numbered from 1."""
        for r, task in enumerate(self.data, start=1):
            mark = "[✓]" if task.get("ok", False) else "[ ]"
            print(f"{r}. {task['name']} : {task['date']} {mark}")

    def add_tasks(self):
        """Adds new tasks from the user to the task list."""
        while True:
            self.print_tasks()
            result = input("Enter Task or Exit :(T/e)")
            if result.lower() == "e":
                return
            elif result.lower() == "t":
                name = input("Enter the Name Task :").strip()
                while not name:
                    name = input("Name can't be empty! Try again :").strip()
                date = input("Enter the Date Task :").strip()
                while not date:
                    date = input("Date can't be empty! Try again :").strip()
                self.data.append({"name": name, "date": date, "ok": False})
            else:
                print("Invalid choice, please enter T or e ")

    def show_tasks(self):
        """Displays your task list"""
        if not self.data:
            print(MSG_NO_TASKS)
        else:
            self.print_tasks()
            input("Enter to Exit")

    def mark_task(self):
        """Mark completed tasks."""
        if not self.data:
            print(MSG_NO_TASKS)
            return
        while True:
            self.print_tasks()
            print(f"{len(self.data) + 1}. Exit")
            try:
                n = int(input("Enter Number of Tasks done or Exit :"))
                if n == len(self.data) + 1:
                    return
                elif n < 1 or n > len(self.data):
                    print(MSG_TASK_NOT_FOUND)
                elif self.data[n - 1]["ok"]:
                    print("This is done !!")
                else:
                    self.data[n - 1]["ok"] = True
            except ValueError:
                print(MSG_INVALID_NUMBER)

    def delete_task(self):
        """Deleting tasks from the task list."""
        if not self.data:
            print(MSG_NO_TASKS)
            return

        while True:
            self.print_tasks()
            print(f"{len(self.data) + 1}. Exit")
            try:
                n = int(input("Enter Number of Tasks you want delete it or Exit :"))
                if n == len(self.data) + 1:
                    return
                elif n < 1 or n > len(self.data):
                    print(MSG_TASK_NOT_FOUND)
                else:
                    self.data.pop(n - 1)
            except ValueError:
                print(MSG_INVALID_NUMBER)

    @staticmethod
    def looks_like_task(task):
        """A task must at least have a name that is real text."""
        return isinstance(task.get("name"), str) and task["name"].strip() != ""

    def save(self, path="tasks.json"):
        """To save your task list"""
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
        os.replace(tmp, path)

    def load(self, path="tasks.json"):
        """To get saved data in file json"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError:
            stamp = time.strftime("%Y%m%d-%H%M%S")
            os.rename(path, f"{path}.corrupted-{stamp}")
            print("Warning: tasks.json was corrupted. Backed it up, starting fresh.")
            self.data = []
        if not isinstance(self.data, list):
            self.data = [self.data]

        good = []
        bad = []
        for task in self.data:
            if isinstance(task, dict) and self.looks_like_task(task):
                task.setdefault("ok", False)
                task.setdefault("date", "undefined")
                good.append(task)
            else:
                bad.append(task)
        self.data = good

        if bad:
            with open(path + ".corrupted", "a", encoding="utf-8") as f:
                for item in bad:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

            print(f"Warning: {len(bad)} broken item(s) moved to quarantine.")


manager = Controller()
manager.load()
while True:
    print(
        "===== Task Manager =====\n\n1. Add task\n2. Show tasks\n3. Mark task as done\n4. Delete task \n5. Exit"
    )
    try:
        num = int(input("Choose :"))
        if num == 1:
            manager.add_tasks()
            manager.save()
        elif num == 2:
            manager.show_tasks()
        elif num == 3:
            manager.mark_task()
            manager.save()
        elif num == 4:
            manager.delete_task()
            manager.save()
        elif num == 5:
            break
        else:
            print("Error number not found")
    except ValueError:
        print(MSG_INVALID_NUMBER)
manager.save()
