# create a tkinter frontend for locking and unlocking the folder


import os
import tkinter as tk
import tkinter.ttk as ttk
import ttkthemes
from tkinter import filedialog, messagebox
from locker import lock_folder, unlock_folder
import threading
import shutil

class FolderLockingWidget(tk.Frame):
    # Folder locking widget
    # This is a sub Widget is used to lock the folder
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.folder_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.create_widgets()
        # responsive
        self.pack(expand=True, fill="both")


    def create_widgets(self):
        # Create the widgets
        # Create the folder selection widgets
        folder_frame = ttk.Frame(self)
        folder_frame.pack(fill="x", expand=True)
        ttk.Label(folder_frame, text="Folder").pack(side="left")
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var)
        self.folder_entry.pack(side="left", expand=True, fill="x")
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side="right")

        # Create the password entry widgets
        password_frame = ttk.Frame(self)
        password_frame.pack(fill="x", expand=True)
        ttk.Label(password_frame, text="Password").pack(side="left")
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(side="left", expand=True, fill="x")

        # Create the lock button
        self.lock_button = ttk.Button(self, text="Lock", command=self.lock)
        self.lock_button.pack()

        self.status_label = ttk.Label(self, text="", foreground="green")
        self.status_label.pack()


    def browse_folder(self):
        # Browse the folder
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def lock(self):
        # Lock the folder
        folder = self.folder_var.get()
        password = self.password_var.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder")
            return
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        self.lock_folder(folder, password)

    def lock_folder(self, folder, password):
        # disable the lock button
        self.lock_button.config(state="disabled")
        self.status_label.config(text="Locking folder...")
        # Lock the folder in a new thread
        self.lock_thread = threading.Thread(target=self._lock_folder, args=(folder, password), daemon=True)
        self.lock_thread.start()


    def _lock_folder(self, folder, password):
        # Lock the folder
        try:
            locked_file = lock_folder(folder, password)
            messagebox.showinfo("Success", f"Folder locked to {locked_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.lock_button.config(state="normal") 
            shutil.rmtree(folder)
            self.status_label.config(text="")



class FolderUnlockingWidget(tk.Frame):
    # Folder unlocking widget
    # This is a sub Widget is used to unlock the folder
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.out_folder_var = tk.StringVar(value=".")
        self.create_widgets()
        # responsive
        self.pack(expand=True, fill="both")

    def create_widgets(self):
        # Create the widgets
        # Create the file selection widgets
        file_frame = ttk.Frame(self)
        file_frame.pack(fill="x", expand=True)
        ttk.Label(file_frame, text="File").pack(side="left")
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var)
        self.file_entry.pack(side="left", expand=True, fill="x")
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side="right")

        # Create the output folder selection widgets
        out_folder_frame = ttk.Frame(self)
        out_folder_frame.pack(fill="x", expand=True)
        ttk.Label(out_folder_frame, text="Output Folder").pack(side="left")
        self.out_folder_entry = ttk.Entry(out_folder_frame, textvariable=self.out_folder_var)
        self.out_folder_entry.pack(side="left", expand=True, fill="x")
        ttk.Button(out_folder_frame, text="Browse", command=self.browse_out_folder).pack(side="right")

        # Create the password entry widgets
        password_frame = ttk.Frame(self)
        password_frame.pack(fill="x", expand=True)
        ttk.Label(password_frame, text="Password").pack(side="left")
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(side="left", expand=True, fill="x")

        # Create the unlock button
        self.unlock_button = ttk.Button(self, text="Unlock", command=self.unlock)
        self.unlock_button.pack()

        self.status_label = ttk.Label(self, text="", foreground="green")
        self.status_label.pack()


    def browse_out_folder(self):
        # Browse the output folder
        folder = filedialog.askdirectory()
        if folder:
            self.out_folder_var.set(folder)

    def browse_file(self):
        # Browse the file
        file = filedialog.askopenfilename()
        if file:
            self.file_var.set(file)
            self.out_folder_var.set(os.path.dirname(file))

    def unlock(self):
        # Unlock the folder
        file = self.file_var.get()
        password = self.password_var.get()
        out_folder = self.out_folder_var.get()

        if not file:
            messagebox.showerror("Error", "Please select a file")
            return
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        self.unlock_folder(file, password, out_folder)

    def unlock_folder(self, file, password, out_folder):
        # disable the unlock button
        self.unlock_button.config(state="disabled")
        self.status_label.config(text="Unlocking folder...")
        # Unlock the folder in a new thread
        self.unlock_thread = threading.Thread(target=self._unlock_folder, args=(file, password, out_folder), daemon=True)
        self.unlock_thread.start()



    def _unlock_folder(self, file, password, out_folder):
        # Unlock the folder
        try:
            unlocked_folder = unlock_folder(file, password, out_folder=out_folder)
            messagebox.showinfo("Success", f"Folder unlocked to {unlocked_folder}")
        except ValueError as e:
            messagebox.showerror("Error", "password is incorrect")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.unlock_button.config(state="normal")
            self.status_label.config(text="")

class MainApplication(ttkthemes.ThemedTk):
    # Main application
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Folder Locker")
        self.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        # Create the widgets
        # Create the notebook
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Create the folder locking widget
        folder_locking_widget = FolderLockingWidget(notebook)
        notebook.add(folder_locking_widget, text="Lock Folder")

        # Create the folder unlocking widget
        folder_unlocking_widget = FolderUnlockingWidget(notebook)
        notebook.add(folder_unlocking_widget, text="Unlock Folder")



if __name__ == "__main__":
    app = MainApplication(theme="arc")
    app.mainloop()
