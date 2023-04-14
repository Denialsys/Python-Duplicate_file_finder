import os
import tkinter as tk
import hashlib
import time

separator = '----------------------'
has_terminated = False

def terminate():
    root.destroy()

def delete_file():
    selection = listbox.curselection()
    if selection:
        filename = listbox.get(selection[0])
        listbox.delete(selection)
        if separator not in filename:
            os.remove(filename)
            print(f'Deleting {filename}')

def update_listbox():
    listbox.delete(0, tk.END)
    target_dir = entry.get()
    files = {}
    duplicate_counter = 0
    file_counter = 0

    time_stamp = time.time()
    report_interval = .05

    if target_dir:
        for main_dir, dirs, filenames in os.walk(target_dir):
            for filename in filenames:
                if has_terminated:
                    return

                path = os.path.join(main_dir, filename)
                hash_sha = hashlib.sha256()
                with open(path, "rb") as f:
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        hash_sha.update(chunk)
                file_hash = hash_sha.digest()

                if file_hash in files:
                    files[file_hash].append(path)
                    duplicate_counter += 1
                else:
                    files[file_hash] = [path]

                file_counter += 1

                if time.time() - time_stamp > report_interval:
                    progress_label.config(text=f"Files scanned: {file_counter}")
                    duplicate_label.config(text=f"Duplicates found: {duplicate_counter}")
                    root.update()
                    time_stamp = time.time()

        progress_label.config(text=f"Total files scanned: {file_counter}")
        duplicate_label.config(text=f"Total Duplicates found: {duplicate_counter}")

        for hash_sha in files:
            if len(files[hash_sha]) > 1:
                for duplicated_file in files[hash_sha]:
                    listbox.insert(tk.END, duplicated_file)
                listbox.insert(tk.END, separator)


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

progress_label = tk.Label(root, text=f"Files scanned: 0")
progress_label.pack(pady=5)

duplicate_label = tk.Label(root, text=f"Duplicates found: 0")
duplicate_label.pack(pady=5)

delete_button = tk.Button(
    root,
    text="Delete File",
    command=delete_file,
    height=1,
    width=10,
)
delete_button.pack(
    side=tk.TOP,
    padx=10,
    pady=10
)

close_button = tk.Button(
    root,
    text="Close",
    command=root.destroy,
    height=1,
    width=10
)

close_button.pack(pady=20)

update_listbox()
root.bind("<Delete>", lambda event: delete_file())
root.mainloop()