import typer
import json
import datetime
from typing_extensions import Annotated

currentTime = datetime.datetime.now()

def main(
        command: Annotated[str,typer.Argument(help="Choose between adding, updating or deleting a task",rich_help_panel="Main Functions",default=...)],
        taskname:Annotated[str,typer.Option(help="Name of task",rich_help_panel="Secondary")] = "",
        taskId: Annotated[int,typer.Option(help="task id at hand",rich_help_panel="Secondary")] = 0,
        status: Annotated[str,typer.Option(help="Change task status to either in progress,done,incomplete",rich_help_panel="Secondary")] = "",
        option: Annotated[str,typer.Option(help="Pick to change either status or name",rich_help_panel="Secondary")] = "",
        newvalue: Annotated[str,typer.Option(help="New value to replace with", rich_help_panel="Secondary")] = ""
    ):
    if command.lower() == "add task" or command.lower() == "add":
        if taskname == "":
            typer.echo("The taskName should have a value")
            typer.Exit(0)
        else:
            try:
                with open("data.json",mode="r",encoding="utf-8") as read_file:
                    data = json.load(read_file)
                    if (data and isinstance(data,list)) or len(data) == 0:
                        print("in here")
                        object = {
                            "Id":len(data) + 1,
                            "Task":taskname,
                            "Status":status,
                            "Created at":str(currentTime),
                            "Updated at":str(currentTime)      
                        }
                        data.append(object)
                        print(data)
                        with open("data.json",mode="w+",encoding="utf-8") as writeFile:
                            json.dump(data,writeFile,indent=4)
                            typer.echo(
                                typer.style("Added task successfully",fg=typer.colors.CYAN,underline=True,italic=True)
                            )
            except json.JSONDecodeError:
                print("JSON file is empty")
                data = [{
                    "Id":1,
                    "Task":taskname,
                    "Status":status,
                    "Created at":str(currentTime),
                    "Updated at":str(currentTime)      
                }]
                with open("data.json","w",encoding="utf-8") as writeFile:
                    if data:
                        json.dump(data,writeFile,indent=4)
                        print("Added task to the file")
                    else:
                        print("Data is empty")
            except FileNotFoundError:
                with open("data.json",mode="x",encoding="utf-8") as createFile:
                    data = [{
                        "Id":1,
                        "Task":taskname,
                        "Status":status,
                        "Created at":str(currentTime),
                        "Updated at":str(currentTime)    
                    }]
                    json.dump(data,createFile,indent=4)
                    typer.echo(
                        typer.style("File created and data inserted",fg=typer.colors.BRIGHT_GREEN,underline=True,bold=True)
                    )
    elif command.lower() == "list" or command.lower() == "list tasks":
        try:
            with open("data.json",mode="r",encoding="utf-8") as read_file:
                try:
                    Data = json.load(read_file)
                    print(Data)
                    if Data and isinstance(Data,list):
                        print(status)
                        filteredData = []
                        for task in Data:
                            if status.lower() == "complete":
                                filteredData = list(filter(lambda values:values['Status'] == "Complete",Data))
                            elif status.lower() == "incomplete":
                                filteredData = list(filter(lambda values:values['Status'] == "Incomplete",Data))
                            elif status.lower() == "in progress":
                                filteredData = list(filter(lambda values: values['Status'] == "In progress",Data))
                            else: filteredData = Data
                        if len(filteredData) > 0:
                            for tasks in filteredData:
                                print("-----------------------")
                                for key,value in tasks.items():
                                    if key == "Status":
                                        if str(value).lower() == "complete":
                                            typer.echo(
                                                typer.style(f"{key} : ") +
                                                typer.style(f"{value}",fg=typer.colors.BRIGHT_GREEN,underline=True,italic=True)
                                            )
                                            continue
                                        elif str(value).lower() == "incomplete":
                                            typer.echo(
                                                typer.style(f"{key} : ") +
                                                typer.style(f"{value}",fg=typer.colors.BRIGHT_RED,underline=True,italic=True)
                                            )
                                            continue
                                        elif str(value).lower() == "in progress":
                                            typer.echo(
                                                typer.style(f"{key} : ") +
                                                typer.style(f"{value}",fg=typer.colors.BRIGHT_CYAN,underline=True,italic=True)
                                            )
                                            continue
                                        else:
                                            typer.echo(
                                                typer.style(f"{key}") + 
                                                typer.style("Invalid",fg=typer.colors.BRIGHT_BLACK,underline=True,italic=True)
                                            )
                                            continue
                                    typer.echo(
                                        typer.style(f"{key} : ") + 
                                        typer.style(f"{value}",fg=typer.colors.BRIGHT_BLUE)
                                    )
                                print("-----------------------")
                    else:
                        typer.echo(typer.style("No tasks present in storage, create some first",bold=True,underline=True))
                except json.JSONDecodeError as error:
                    print(error)
                    typer.echo(
                        typer.style("No tasks added, enter in some tasks to list them out next time",fg=typer.colors.BRIGHT_MAGENTA,underline=True)
                    )
        except FileNotFoundError as error:
            print(error)
    elif command.lower() == "update" or command.lower() == "update tasks":
        changed = False
        with open("data.json",mode="r",encoding="utf-8") as read_file:
            try:
                data = json.load(read_file)
                if data:
                    for task in data:
                        if task["Id"] == taskId:
                            if option == "name":
                                if newvalue != None:
                                    task["Task"] = newvalue
                                    task["Updated at"] = str(currentTime)
                                    changed = True
                                    break
                                else:
                                    typer.echo("No new value entered")
                                    typer.Abort(1)
                            elif option == "Status":
                                if newvalue != None:
                                    changed = True
                                    task["Status"] = newvalue
                                    task["Updated at"] = str(currentTime)
                                    break
                                else:
                                    typer.echo("No new value entered")
                                    typer.Abort(1)
                            else:
                                typer.echo("Invalid option provided")
                                typer.Abort(1)
                    if not changed:
                        typer.echo(
                            typer.style("No such task exists")
                        )
                    with open("data.json",mode="w",encoding="utf-8") as writeFile:
                        json.dump(data,writeFile,indent=4)
                        typer.echo(
                            typer.style("Value updated",fg=typer.colors.BRIGHT_BLUE,underline=True)
                        )
            except json.JSONDecodeError:
                typer.echo(
                    typer.style("No tasks made, create some tasks first",fg=typer.colors.BRIGHT_RED)
                )
    elif command.lower() == "delete" or command.lower() == "delete tasks":
        with open("data.json",mode="r",encoding="utf-8") as read_file:
            try:
                deleted = False
                data = json.load(read_file)
                if data:
                    for task in data:
                        if task["Id"] == taskId:
                            data.pop(taskId - 1)
                            deleted = True
                            break
                    if deleted:
                        newId = 1
                        for task in data:
                            task["Id"] = newId
                            newId += 1
                        typer.echo(
                            typer.style("Value deleted",fg=typer.colors.BRIGHT_BLUE,underline=True)
                        )
                        with open("data.json",mode="w",encoding="utf-8") as writeFile:
                            json.dump(data,writeFile,indent=4)
                    else:
                        typer.echo(
                            typer.style("No task of that id exists",typer.colors.BRIGHT_RED,underline=True)
                        )
                else:
                    typer.echo(
                        typer.style("No tasks created, enter some first to delete",typer.colors.BRIGHT_BLACK,underline=True)
                    )
            except json.JSONDecodeError:
                typer.echo(
                    typer.style("No tasks created, enter some first to delete",typer.colors.BRIGHT_BLACK,underline=True)
                )

if __name__ == "__main__":
    typer.run(main)