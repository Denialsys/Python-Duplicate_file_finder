import os
import tkinter as tk

def delete_file(filename):
    os.remove(filename)
    listbox.delete(listbox.curselection())
    print(f'Removed: {filename}')

def update_listbox():
    listbox.delete(0, tk.END)
    target_dir = entry.get()
    if target_dir:
        for dirpath, dirnames, filenames in os.walk(target_dir):

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                if os.path.isfile(file_path):
                    listbox.insert(tk.END, file_path)

root = tk.Tk()
root.geometry("1000x700")
root.title("File duplicate finder")

listbox = tk.Listbox(root)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

label = tk.Label(root, text="Target directory:")
label.pack(side=tk.TOP, padx=10, pady=5)

entry = tk.Entry(root)
entry.pack(side=tk.TOP, padx=10, pady=5)

update_button = tk.Button(
    root,
    text="Update List",
    command=update_listbox,
    height=1,
    width=10
)
update_button.pack(
    side=tk.TOP,
    padx=10,
    pady=10
)
delete_button = tk.Button(
    root,
    text="Delete File",
    command=lambda: delete_file(listbox.get(listbox.curselection())),
    height=1,
    width=10,
)
delete_button.pack(
    side=tk.TOP,
    padx=10,
    pady=10
)

update_listbox()
root.bind("<Delete>", lambda event: delete_file(listbox.get(listbox.curselection())))
root.mainloop()