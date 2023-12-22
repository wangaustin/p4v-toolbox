#!/usr/bin/env python

import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

import subprocess
import time
import sys
import json
import codecs
import os

# get the absolute path of where this script is located
this_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------
# FUNCTION: ask directory
# ----------------------------------
def func_ask_directory():
	label_file_explorer = filedialog.askdirectory()
	folder_path.set(label_file_explorer)
    
# ----------------------------------
# FUNCTION: generate json
# ----------------------------------
def func_generate_json():
    if not ent_username.get():
        user_warning.set("Please enter a username!")
        return
    
    if not folder_path.get():
        user_warning.set("Please select workspace folder!")
        return
    
    # get powershell file directory
    script_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.'

    # specify path to powershell script file
    ps_script_file = f'{script_dir}/generate_json.ps1'
    
    username = ent_username.get()

    # run PowerShell script with the username as an argument
    subprocess.Popen(['powershell', '-File', ps_script_file, '-Username', username], cwd=script_dir, shell=True)
    
    user_warning.set("Successfully generated JSON.")
    
# ----------------------------------
# FUNCTION: show stats
# ----------------------------------
def func_show_stats():
    json_file_path = os.path.join(this_directory, 'changelists.json')
    
    try:
        with codecs.open(json_file_path, 'r', encoding='utf-8-sig') as file:
            file_content = file.read()

            if not file_content:
                user_stats.set("JSON file is empty.")
                return

            data = json.loads(file_content)
            num_entries = len(data)
            user_stats.set('Count: ' + str(num_entries))

    except FileNotFoundError:
        user_stats.set(f"JSON file not found at path: {json_file_path}")

    except json.JSONDecodeError as e:
        user_stats.set(f"Error decoding JSON: {e}")

    except Exception as e:
        user_stats.set(f"Error: {e}")


# ------------------------
# Root Frame UI
# ------------------------

# root
root = Tk()
root.title("Little P4V Toolbox")

#greeting
greeting = Label(
    root,
    justify="left",
    text="Welcome to Little P4V Toolbox! Make sure you're connected to Perforce first."
)
greeting.grid(row=0, column=0, sticky="n")

# username entry
label_username = Label(
    root,
    text="Username in Depot:"
)
label_username.grid(row=1, column=0, sticky="n")

ent_username = Entry(root, bd=5)
ent_username.grid(row=2, column=0, columnspan=2, sticky="n")

# folder path button
folder_path = StringVar()
button_ask_directory = Button(root, text="Workspace Folder...", command=func_ask_directory)
button_ask_directory.grid(row=3, column=0, sticky="n")

label_file_list = Label(root, textvariable=folder_path, width=70, height=2, fg = "blue")
label_file_list.grid(row=4, column=0, sticky="w")

user_warning = StringVar()
label_warning = Label(root, textvariable=user_warning, width=70, height=2, fg="red")
label_warning.grid(row=5, column=0, sticky="w")

button_generate_json = Button(root, text="Generate JSON", command=func_generate_json)
button_generate_json.grid(row=6, column=0, sticky="n")

stats_warning = Label(root, text="WARNING: Generate JSON first before getting stats.", width=70, height=4, fg="red")
stats_warning.grid(row=7, column=0, sticky="w")

button_show_stats = Button(root, text="Show Stats", command=func_show_stats)
button_show_stats.grid(row=8, column=0, sticky="n")

user_stats = StringVar()
label_stats = Label(root, textvariable=user_stats, width=70, height=4, fg="blue")
label_stats.grid(row=9, column=0, sticky="n")



root.mainloop()