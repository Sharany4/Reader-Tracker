#import the tkinter library
#from tkinter import *
import tkinter as tk
import random

#Create the root window
root = tk.Tk()

#change the root window background
root.configure(bg="white")

#changethe root title
root.title("My awesome to do list")

#Change the window size
root.geometry("200x500")


#create functions
def add_task():
    pass #makes an empty function

def del_task():
    pass

def del_all():
    pass

def del_one():
    pass

def sort_asc():
    pass

def sort_desc():
    pass

def choose_random():
    pass

def show_number_of_tasks():
    pass






#addthe title
root.title("To do list")


#add a label
lbl_title  = tk.Label(root, text = "to do list", bg = "white")
lbl_title.pack()

#add a label display
lbl_display  = tk.Label(root, text = "", bg = "white")
lbl_display.pack()

#make buttons
txt_input = tk.Entry(root, width=15)
txt_input.pack()

btn_add_task = tk.Button(root, text="Add task", fg = "green", bg = "white", command=add_task)
btn_add_task.pack()

btn_del_all = tk.Button(root, text="Delete all", fg = "green", bg = "white", command=del_all)
btn_del_all.pack()

btn_del_one = tk.Button(root, text="Delete one", fg = "green", bg = "white", command=del_one)
btn_del_one.pack()

btn_sort_asc = tk.Button(root, text="Sort ascending", fg = "green", bg = "white", command=sort_asc)
btn_sort_asc.pack()

btn_sort_desc = tk.Button(root, text="Sort descending", fg = "green", bg = "white", command=sort_desc)
btn_sort_desc.pack()

btn_choose_random = tk.Button(root, text="Choose random", fg = "green", bg = "white", command=choose_random)
btn_choose_random.pack()

btn_number_of_tasks = tk.Button(root, text="Number of tasks", fg = "green", bg = "white", command=show_number_of_tasks)
btn_number_of_tasks.pack()

btn_exit = tk.Button(root, text="Quit", fg = "green", bg = "white", command=exit)
btn_exit.pack()

lb_tasks = tk.Listbox(root)
lb_tasks.pack()


#Start the main events loop
root.mainloop()

