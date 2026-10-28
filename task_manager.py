import json


class Controller:
    def __init__(self, data=None):
        self.data = data if data is not None else []

    def Add_Tasks(self):
        while True:
            result = input("Enter Task or Exit :(T/e)")
            if result.lower() == "e":
                return
            elif result.lower() == "t":
                name = input("Enter the Name Task :")
                date = input("Enter the Date Task :")
                self.data.append({"name": name, "date": date, "ok": False})
            else:
                print("Invalid choice, please enter T or e ")

    def Show_Tasks(self):
        if not self.data:
            print("You dot`n have any Tasks :)")
        else:
            r = 1
            for task in self.data:
                if not task["ok"]:
                    print(f"{r}. {task['name']} : {task['date']}[]")
                else:
                    print(f"{r}. {task['name']} : {task['date']}[✓]")
                r += 1
        e = input("Exit(E)").lower()
        if e == "e":
            return
        else:
            return

    def Mark_Task(self):
        if not self.data:
            print("You dot`n have any Tasks :)")
            return
        while True:
            r = 1
            for task in self.data:
                if not task["ok"]:
                    print(f"{r}. {task['name']} : {task['date']}[]")
                else:
                    print(f"{r}. {task['name']} : {task['date']}[✓]")
                r += 1
            print(f"{len(self.data) + 1}. Exit")
            try:
                n = int(input("Enter Number of Tasks doen or Exit :"))
                if n <= len(self.data) and not self.data[n - 1]["ok"]:
                    self.data[n - 1]["ok"] = True
                elif n == len(self.data) + 1:
                    return
                elif self.data[n - 1]["ok"]:
                    print("This is deon !!")
                else:
                    print("Error number not found")
            except ValueError:
                print("TypeError This Not Number !!")

    def Delete_Task(self):
        if not self.data:
            print("You dot`n have any Tasks :)")
            return

        while True:
            r = 1
            for task in self.data:
                if not task["ok"]:
                    print(f"{r}. {task['name']} : {task['date']}[]")
                else:
                    print(f"{r}. {task['name']} : {task['date']}[✓]")
                r += 1
            print(f"{len(self.data) + 1}. Exit")
            try:
                n = int(input("Enter Number of Tasks doen or Exit :"))
                if n <= len(self.data):
                    self.data.pop(n - 1)
                elif n == len(self.data) + 1:
                    return
                else:
                    print("Error number not found")
            except ValueError:
                print("TypeError This Not Number !!")

    def save(self, path="tasks.json"):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def load(self, path="tasks.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []


c = Controller()
c.load()
while True:
    print(
        "===== Task Manager =====\n\n1. Add task\n2. Show tasks\n3. Mark task as done\n4. Delete task \n5. Exit"
    )
    try:
        num = int(input("Choose :"))
        if num == 1:
            c.Add_Tasks()
            c.save()
        elif num == 2:
            c.Show_Tasks()
        elif num == 3:
            c.Mark_Task()
            c.save()
        elif num == 4:
            c.Delete_Task()
            c.save()
        elif num == 5:
            break
        else:
            print("Error number not found")
    except ValueError:
        print("TypeError This Not Number !!")
c.save()
