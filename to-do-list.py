from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_title = task_input.get()
    if len(task_title) == 0:
        messagebox.showerror('Input Error', 'Please enter a task description.')
    else:
        task_list.append(task_title)
        db_cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_title,))
        update_task_list()
        task_input.delete(0, 'end')
def update_task_list():
    clear_task_list()
    for task in task_list:
        task_listbox.insert('end', task)
def remove_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        if selected_task in task_list:
            task_list.remove(selected_task)
            update_task_list()
            db_cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task,))
    except:
        messagebox.showerror('Selection Error', 'Please select a task to remove.')
def remove_all_tasks():
    confirm = messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete all tasks?')
    if confirm:
        task_list.clear()
        db_cursor.execute('DELETE FROM tasks')
        update_task_list()

def clear_task_list():
    task_listbox.delete(0, 'end')

def close_app():
    print("Tasks:", task_list)
    gui_window.destroy()

def fetch_tasks_from_db():
    while len(task_list) != 0:
        task_list.pop()
    for row in db_cursor.execute('SELECT title FROM tasks'):
        task_list.append(row[0])

if __name__ == "__main__":
    gui_window = Tk()
    gui_window.title("To-Do Manager")
    gui_window.geometry("700x450+500+250")
    gui_window.resizable(0, 0)
    gui_window.configure(bg="#D3F4F1")


    connection = sql.connect('task_manager.db')
    db_cursor = connection.cursor()
    db_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')


    task_list = []
    main_frame = Frame(gui_window, bg="#A1D8E5")
    main_frame.pack(side="top", expand=True, fill="both")

    header_label = Label(main_frame, text="Task Manager\nEnter Your Task", font=("Helvetica", 16, "bold"), background="#A1D8E5", foreground="#FF5733")
    header_label.place(x=20, y=20)

    task_input = Entry(main_frame, font=("Helvetica", 14), width=40, bg="white", fg="black")
    task_input.place(x=180, y=25)

    add_button = Button(main_frame, text="Add Task", width=15, bg='#FF8C00', font=("Helvetica", 14, "bold"), command=add_task)
    remove_button = Button(main_frame, text="Remove Task", width=15, bg='#FF8C00', font=("Helvetica", 14, "bold"), command=remove_task)
    clear_button = Button(main_frame, text="Delete All Tasks", width=15, bg='#FF8C00', font=("Helvetica", 14, "bold"), command=remove_all_tasks)
    exit_button = Button(main_frame, text="Exit", width=52, bg='#FF8C00', font=("Helvetica", 14, "bold"), command=close_app)

    add_button.place(x=18, y=80)
    remove_button.place(x=240, y=80)
    clear_button.place(x=460, y=80)
    exit_button.place(x=17, y=320)
    task_listbox = Listbox(main_frame, width=75, height=10, font=("Helvetica", 12, "bold"), selectmode='SINGLE', bg="white", fg="black", selectbackground="#FF8C00", selectforeground="black")
    task_listbox.place(x=20, y=140)
    fetch_tasks_from_db()
    update_task_list()

    gui_window.mainloop()
    connection.commit()
    db_cursor.close()
