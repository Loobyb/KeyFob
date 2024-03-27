import tkinter as tk
from tkinter import messagebox

class myGui:
    def __init__(self):
        # Creation of GUI main window and set title
        self.todo_list = []
        self.main_window = tk.Tk()
        self.main_window.title('Group Project')
        self.main_window.geometry("500x450")
        self.main_frame = tk.Frame(self.main_window, height=1000, width=800)
        self.main_frame.pack()

        # Buttons for creating a new list and importing a task list
        self.newListButton = tk.Button(self.main_frame, text='Create', command=self.newlist_button)
        self.importButton = tk.Button(self.main_frame, text='Import', command=self.import_tasklist)
        self.newListButton.pack(padx=20, pady=(150,10))
        self.importButton.pack(padx=20, pady=10)

        # Help label
        self.info_label_frame = tk.Frame(self.main_frame)
        self.info_label_frame.pack(padx=20, pady=10)
        self.info_label = tk.Label(self.info_label_frame, text='To create a new list, select "Create" then enter a title for the list.' +
                                                               '\nTo import a list select "Import" then enter the text file name.')
        self.info_label.pack(padx=20, pady=10)

    # Frame for creating a new task list
    def newlist_button(self):
        self.createList = tk.Toplevel()
        self.createList.title('List information')
        self.createListFrame = tk.Frame(self.createList)
        self.createListFrame.pack()
        self.listTitle = tk.Label(self.createListFrame, text='Please name the Tasklist:')
        self.listTitle.pack(side='left', pady=10, padx=20)
        self.titleEntry = tk.Entry(self.createListFrame)
        self.titleEntry.pack(side='left', pady=10, padx=20)
        self.buttonFrame = tk.Frame(self.createList)
        self.buttonFrame.pack()
        self.createButton = tk.Button(self.buttonFrame, text='Create', command=self.create_list)
        self.createButton.pack(padx=10, pady=10)

    # Function for creating a new task list
    def create_list(self):
        self.main_frame.pack_forget()
        self.created_list_frame = tk.Frame(self.main_window)
        self.created_list_frame.pack(fill='both', expand=True)
        self.title_label = tk.Label(self.created_list_frame, text=self.titleEntry.get())
        self.createList.destroy()
        self.title_label.pack(side='top')
        self.buttons_frame = tk.Frame(self.created_list_frame)
        self.buttons_frame.pack(padx=10, pady=10, fill="x")
        self.add_button = tk.Button(self.buttons_frame, text='Add Task', command=self.create_add_task_frame)
        self.add_button.pack(side='left', padx=5, pady=5)
        self.update_button = tk.Button(self.buttons_frame, text='Mark as Complete', command=self.update_task)
        self.update_button.pack(side='left', padx=5, pady=5)
        self.delete_button = tk.Button(self.buttons_frame, text='Delete Task', command=self.delete_task_function)
        self.delete_button.pack(side='left',padx=5,pady=5)
        self.quit_button = tk.Button(self.buttons_frame, text='Quit', command=self.quit_button_function)
        self.quit_button.pack(side='right', padx=20, pady=5)

        # Listbox for displaying tasks
        self.listbox_frame = tk.Frame(self.created_list_frame)
        self.listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.vert_scrollbar = tk.Scrollbar(self.listbox_frame, orient='vertical')
        self.hor_scrollbar = tk.Scrollbar(self.listbox_frame, orient='horizontal')
        self.vert_scrollbar.pack(side='right', fill='y')
        self.hor_scrollbar.pack(side='bottom', fill='x')
        self.inner_listbox_frame = tk.Frame(self.listbox_frame)
        self.inner_listbox_frame.pack(fill='both',expand=True)
        self.listbox = tk.Listbox(self.inner_listbox_frame)
        self.vert_scrollbar.config(command=self.listbox.yview)
        self.hor_scrollbar.config(command=self.listbox.xview)
        self.listbox.config(yscrollcommand=self.vert_scrollbar.set,xscrollcommand=self.hor_scrollbar.set)
        self.vert_scrollbar.pack(side='right', fill='y')
        self.hor_scrollbar.pack(side='bottom',fill='x')
        self.listbox.pack(side='left', fill='both', expand=True)

        #Sort and Filter Buttons
        self.function_button_frame = tk.Frame(self.created_list_frame)
        self.function_button_frame.pack(side='left')
        self.sort_button = tk.Button(self.function_button_frame,text='Sort',
                                     command=self.sort_list)
        self.sort_button.pack(side='left',padx=10)
        self.filter_button = tk.Button(self.function_button_frame,text='Filter', command=self.filter_list)
        self.filter_button.pack(side='left',padx=10)
        self.showall_button = tk.Button(self.function_button_frame, text='Show All',
                                        command=self.showall_function)
        self.showall_button.pack(side='left',padx=10)
        # Main menu and Save buttons
        self.main_menu_button_frame = tk.Frame(self.created_list_frame)
        self.main_menu_button_frame.pack(side='right')
        self.main_menu_button = tk.Button(self.main_menu_button_frame, text='Main Menu', command=self.created_main_menu_function)
        self.main_menu_button.pack(side='right', pady=10, padx=10)
        self.save_button_frame = tk.Frame(self.created_list_frame)
        self.save_button_frame.pack(side='right')
        self.save_button = tk.Button(self.save_button_frame, text='Save', command=self.save_button_function)
        self.save_button.pack(side='right', pady=10, padx=10)

    #Function to Delete a task
    def delete_task_function(self):
        selected_index = self.listbox.curselection()
        selected_index = int(selected_index[0])
        result = messagebox.askquestion("Warning",
                                        "Deleting task will permanently remove the task selected. \nDo you want to continue?")
        if result == 'yes':
            self.listbox.delete(selected_index)
            self.todo_list.pop(selected_index)
        else:
            return

    #Function to filter all the done tasks
    def filter_list(self):
        self.listbox.delete(0,tk.END)
        for task in self.todo_list:
            if task['status'] == 'ND':
                if task['priority'] == 'High':
                    background_color = 'red'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                elif task['priority'] == 'Medium':
                    background_color = 'orange'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                else:
                    background_color = 'yellow'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
            else:
                continue

    #Function to Sort the tasklist by priority
    def sort_list(self):
        self.todo_list.sort(key=lambda x: {'High': 0, 'Medium': 1, 'Low': 2}.get(x['priority'], float('inf')))
        self.listbox.delete(0,tk.END)
        for task in self.todo_list:
            if task['status'] == 'D':
                background_color = 'green'
                self.listbox.insert(tk.END,
                                    f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                self.listbox.itemconfig(tk.END, background=background_color)
            else:
                if task['priority'] == 'High':
                    background_color = 'red'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                elif task['priority'] == 'Medium':
                    background_color = 'orange'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                else:
                    background_color = 'yellow'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)

    def showall_function(self):
        self.listbox.delete(0, tk.END)
        for task in self.todo_list:
            if task['status'] == 'D':
                background_color = 'green'
                self.listbox.insert(tk.END,
                                    f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                self.listbox.itemconfig(tk.END, background=background_color)
            else:
                if task['priority'] == 'High':
                    background_color = 'red'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                elif task['priority'] == 'Medium':
                    background_color = 'orange'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)
                else:
                    background_color = 'yellow'
                    self.listbox.insert(tk.END,
                                        f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
                    self.listbox.itemconfig(tk.END, background=background_color)

    # Function for updating task completion status
    def update_task(self):
        selected_index = self.listbox.curselection()
        selected_index = int(selected_index[0])
        task = self.todo_list[selected_index]
        current_background = self.listbox.itemcget(selected_index, 'background')
        new_background = 'red' if current_background == 'green' else 'green'
        task['status'] = 'ND' if current_background == 'green' else 'D'
        self.listbox.delete(selected_index)
        self.listbox.insert(selected_index,
                            f"{task['status']} - Task: {task['name']} - Category: {task['category']} - Priority: {task['priority']} - Description: {task['description']}")
        if new_background == 'red':
            if task['priority'] == 'Medium':
                new_background = 'orange'
            elif task['priority'] == 'Low':
                new_background = 'yellow'
            else:
                new_background = 'red'
        self.listbox.itemconfig(selected_index, background=new_background)

    # Function for adding a new task
    def create_add_task_frame(self):
        self.add_task_window = tk.Toplevel()
        self.add_task_window.title('Add a Task')
        self.task_name_frame = tk.LabelFrame(self.add_task_window, text='NEW TASK')
        self.task_name_frame.pack(padx=10, pady=10)
        self.task_name_label = tk.Label(self.task_name_frame, text='Name:')
        self.task_name_label.pack(side='left', padx=5, pady=5)
        self.task_name_entry = tk.Entry(self.task_name_frame, borderwidth=2)
        self.task_name_entry.pack(side='left', padx=5, pady=5)
        self.category_frame = tk.Frame(self.add_task_window)
        self.category_frame.pack(padx=10, pady=5)
        self.category_label = tk.Label(self.category_frame, text='Category:')
        self.category_label.pack(side='left', padx=5, pady=5)
        self.category_var = tk.StringVar(value='None')
        for cat in ['Work', 'Personal', 'School', 'Misc.']:
            rb = tk.Radiobutton(self.category_frame, text=cat, variable=self.category_var, value=cat)
            rb.pack(side='left', padx=5, pady=5)
        self.priority_frame = tk.Frame(self.add_task_window)
        self.priority_frame.pack()
        self.priority_label = tk.Label(self.priority_frame, text='Priority:')
        self.priority_label.pack(side='left')
        self.priority_var = tk.StringVar(value='None')
        for priority in ['Low', 'Medium', 'High']:
            prior_rb = tk.Radiobutton(self.priority_frame, text=priority, variable=self.priority_var, value=priority)
            prior_rb.pack(side='left', padx=5, pady=5)
        self.description_frame = tk.Frame(self.add_task_window)
        self.description_frame.pack()
        self.description_label = tk.Label(self.description_frame, text='Task Description:')
        self.description_label.pack()
        self.description_entry = tk.Text(self.description_frame, wrap=tk.WORD, width=50, height=5)
        self.description_entry.pack(padx=10, pady=10)
        self.buttons_frame = tk.Frame(self.add_task_window)
        self.buttons_frame.pack(padx=10, pady=10, fill="x")
        self.add_button = tk.Button(self.buttons_frame, text='Add Task', command=self.add_task)
        self.add_button.pack(side='left', padx=5, pady=5)

    # Function for adding a new task to the listbox
    def add_task(self):
        name = self.task_name_entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        status = 'ND'

        if not name:
            messagebox.showwarning('Warning', 'Name field cannot be empty.')
            return
        elif category == 'None':
            messagebox.showwarning('Warning', 'Category field cannot be None.')
            return
        elif priority == 'None':
            messagebox.showwarning('Warning', 'Priority field cannot be None.')
            return
        elif not description:
            messagebox.showwarning('Warning', 'Description field cannot be None.')
            return

        self.todo_list.append({'name':name,'status':status,'category':category,'priority':priority,'description':description})
        self.listbox.insert(tk.END,
                            f"{status} - Task: {name} - Category: {category} - Priority: {priority} - Description: {description}")
        if priority == "High":
            self.listbox.itemconfigure(tk.END, background='red')
        elif priority == "Medium":
            self.listbox.itemconfigure(tk.END, background='orange')
        else:
            self.listbox.itemconfigure(tk.END, background='yellow')
        self.add_task_window.destroy()

    # Function for handling the 'Quit' button
    def quit_button_function(self):
        result = messagebox.askquestion("Warning",
                                        "Without saving, your task list progress will be lost. Do you want to continue?")
        if result == 'yes':
            self.main_window.destroy()
        else:
            return

    # Function for handling the 'Save' button#self.current_directory +
    def save_button_function(self):
        file_name = self.title_label.cget('text')
        listbox_contents = self.listbox.get(0, tk.END)
        with open(file_name.lower() + '.txt', 'w') as file:
            for item in listbox_contents:
                file.write(item + "\n")
        messagebox.showinfo("Save Success", "Your file was saved succesfully.")

    # Function for returning to the main menu
    def created_main_menu_function(self):
        result = messagebox.askquestion("Warning",
                                        "Without saving, your task list progress will be lost. Do you want to continue?")
        if result == 'yes':
            self.todo_list.clear()
            self.main_frame.pack()
            self.created_list_frame.pack_forget()
        else:
            return

        # Function for returning to the main menu

    def import_main_menu_function(self):
        result = messagebox.askquestion("Warning",
                                        "Without saving, your task list progress will be lost. Do you want to continue?")
        if result == 'yes':
            self.todo_list.clear()
            self.import_list_frame.pack_forget()
            self.main_frame.pack()
        else:
            return

    # Function for importing a task list
    def import_tasklist(self):
        self.import_list = tk.Toplevel()
        self.import_list.title('List information')
        self.import_frame = tk.Frame(self.import_list)
        self.import_frame.pack()
        self.import_title = tk.Label(self.import_frame, text='Enter the To-Do list Name you want to import:')
        self.import_title.pack(side='left', pady=10, padx=20)
        self.import_entry = tk.Entry(self.import_frame)
        self.import_entry.pack(side='left', pady=10, padx=20)
        self.import_button_frame = tk.Frame(self.import_list)
        self.import_button_frame.pack()
        self.import_button = tk.Button(self.import_button_frame, text='Import', command=self.import_function)
        self.import_button.pack(padx=10, pady=10)

    # Function for handling the import process
    def import_function(self):
        import_file = self.import_entry.get().strip().lower()

        print("Attempting to open file:", import_file + '.txt')
        try:
            # Try to open the file
            with open(import_file + ".txt", 'r') as file:
                # Read the contents of the file and add tasks to the todo_list
                for line in file:
                    # Parse the line to extract task information
                    # Assuming each line has the format: "Status: D - Task: ... - Category: ... - Priority: ... - Description: ..."
                    status, name, category, priority, description = line.strip().split(' - ')
                    status = status.strip()
                    name = name.split(': ')[1]
                    category = category.split(': ')[1]
                    priority = priority.split(': ')[1]
                    description = description.split(': ')[1]
                    # Add the task to todo_list
                    self.todo_list.append({'status': status, 'name': name, 'category': category, 'priority': priority,
                                           'description': description})
        except FileNotFoundError:
            # If the file is not found, show a messagebox error
            messagebox.showerror("Error", "File not found. Please enter a correct file name.")
            return
        self.main_frame.pack_forget()
        self.import_list_frame = tk.Frame(self.main_window)
        self.import_list_frame.pack(fill='x', expand=True)
        self.title_label = tk.Label(self.import_list_frame, text=import_file)
        self.import_list.destroy()
        self.title_label.pack(side='top')
        self.import_buttons_frame = tk.Frame(self.import_list_frame)
        self.import_buttons_frame.pack(padx=10, pady=10, fill="x")
        self.add_button = tk.Button(self.import_buttons_frame, text='Add Task', command=self.create_add_task_frame)
        self.add_button.pack(side='left', padx=5, pady=5)
        self.update_button = tk.Button(self.import_buttons_frame, text='Mark as Complete', command=self.update_task)
        self.update_button.pack(side='left', padx=5, pady=5)
        self.delete_button = tk.Button(self.import_buttons_frame, text='Delete Task', command=self.delete_task_function)
        self.delete_button.pack(side='left', padx=5, pady=5)
        self.quit_button = tk.Button(self.import_buttons_frame, text='Quit', command=self.quit_button_function)
        self.quit_button.pack(side='right', padx=20, pady=5)

        # Listbox for displaying tasks
        self.listbox_frame = tk.Frame(self.import_list_frame)
        self.listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.vert_scrollbar = tk.Scrollbar(self.listbox_frame, orient='vertical')
        self.hor_scrollbar = tk.Scrollbar(self.listbox_frame, orient='horizontal')
        self.vert_scrollbar.pack(side='right', fill='y')
        self.hor_scrollbar.pack(side='bottom', fill='x')
        self.inner_listbox_frame = tk.Frame(self.listbox_frame)
        self.inner_listbox_frame.pack(fill='both', expand=True)
        self.listbox = tk.Listbox(self.inner_listbox_frame)
        self.vert_scrollbar.config(command=self.listbox.yview)
        self.hor_scrollbar.config(command=self.listbox.xview)
        self.listbox.config(yscrollcommand=self.vert_scrollbar.set, xscrollcommand=self.hor_scrollbar.set)
        self.vert_scrollbar.pack(side='right', fill='y')
        self.hor_scrollbar.pack(side='bottom', fill='x')
        self.listbox.pack(side='left', fill='both', expand=True)

        # Sort and Filter Buttons
        self.function_button_frame = tk.Frame(self.import_list_frame)
        self.function_button_frame.pack(side='left')
        self.sort_button = tk.Button(self.function_button_frame, text='Sort',
                                     command=self.sort_list)
        self.sort_button.pack(side='left',padx=10)
        self.filter_button = tk.Button(self.function_button_frame, text='Filter',
                                       command=self.filter_list)
        self.filter_button.pack(side='left',padx=10)
        self.showall_button = tk.Button(self.function_button_frame, text='Show All',
                                        command=self.showall_function)
        self.showall_button.pack(side='left',padx=10)

        # Main menu and Save buttons
        self.main_menu_button_frame = tk.Frame(self.import_list_frame)
        self.main_menu_button_frame.pack(side='right')
        self.main_menu_button = tk.Button(self.main_menu_button_frame, text='Main Menu',
                                          command=self.import_main_menu_function)
        self.main_menu_button.pack(side='right', pady=10, padx=10)
        self.save_button_frame = tk.Frame(self.import_list_frame)
        self.save_button_frame.pack(side='right')
        self.save_button = tk.Button(self.save_button_frame, text='Save', command=self.save_button_function)
        self.save_button.pack(side='right', pady=10, padx=10)

        self.listbox.delete(0, tk.END)
        for item in self.todo_list:
            self.listbox.insert(tk.END,
                                f"{item['status']} - Task: {item['name']} - Category: {item['category']} - Priority: {item['priority']} - Description: {item['description']}")
            if item['priority'] == "High":
                self.listbox.itemconfigure(tk.END, background='red')
            elif item['priority'] == "Medium":
                self.listbox.itemconfigure(tk.END, background='orange')
            else:
                self.listbox.itemconfigure(tk.END, background='yellow')
            if item['status'] == 'D':
                self.listbox.itemconfigure(tk.END, background='green')

if __name__ == '__main__':
    mygui = myGui()
    tk.mainloop()