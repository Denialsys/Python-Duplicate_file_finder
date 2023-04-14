import os
import tkinter as tk
import hashlib
import time

separator = '----------------------'

def delete_file():
    selection = listbox.curselection()
    if selection:
        filename = listbox.get(selection[0])
        # os.remove(filename)
        listbox.delete(selection)

def update_listbox():
    listbox.delete(0, tk.END)
    target_dir = entry.get()
    files = {}
    duplicate_counter = 0
    file_counter = 0

    time_stamp = time.time()
    report_interval = .05

    if target_dir:
        for root, dirs, filenames in os.walk(target_dir):
            for filename in filenames:
                path = os.path.join(root, filename)

                with open(path, "rb") as f:
                    file_hash = hashlib.md5(f.read(1024)).hexdigest()

                if file_hash in files:
                    files[file_hash].append(path)
                    duplicate_counter += 1
                else:
                    files[file_hash] = [path]

                file_counter += 1

                # if time.time() - time_stamp > report_interval:
                #     progress_label.config(text=f"{progress}%")
                #     root.update()
                #     report_interval = time.time()
        print(files)
        for hash in files:
            if len(files[hash]) > 1:
                for duplicated_file in files[hash]:
                    listbox.insert(tk.END, duplicated_file)
                listbox.insert(tk.END, separator)
        # for filename in os.listdir():
        #     if os.path.isfile(filename):


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

update_button = tk.Button(root, text="Update List", command=update_listbox)
update_button.pack(side=tk.TOP, padx=10, pady=5)

delete_button = tk.Button(root, text="Delete File", command=delete_file)
delete_button.pack(side=tk.TOP, padx=10, pady=5)

update_listbox()

root.bind("<Delete>", lambda event: delete_file())
root.mainloop()