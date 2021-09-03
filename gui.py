from tkinter import *
from functools import partial
from functionalities.LogManipulation import *

window = Tk()
window.title("Log Manipulator")
window.geometry('400x400')

# fields

# input file
label_inputpath_text = Label(window, text="Input Path: ")
label_inputpath_text.grid(column=0, row=0)
label_inputpath_entry = Entry(window)
label_inputpath_entry.grid(column=1, row=0)

# output file
label_outputpath_text = Label(window, text="Output Path: ")
label_outputpath_text.grid(column=0, row=1)
label_outputpath_entry = Entry(window)
label_outputpath_entry.grid(column=1, row=1)

# dqis
label_dqis_text = Label(window, text="DQI(s) to insert: ")
label_dqis_text.grid(column=0, row=2)

list_dqis = Listbox(window, selectmode="multiple")
list_dqis.grid(column=1, row=2)

i = 1
while i <= 27:
    item_string = "I" + str(i)
    list_dqis.insert(END, item_string)
    i = i + 1

yscrollbar = Scrollbar(window)
yscrollbar.grid(column=2, row=2, sticky='NSW')
yscrollbar.config(command=list_dqis.yview)

# amount of dqis
label_amountabs_text = Label(window, text="Absolute* DQI(s): ")
label_amountabs_text.grid(column=0, row=3)
label_amountabs_entry = Entry(window)
label_amountabs_entry.grid(column=1, row=3)

label_amountrel_text = Label(window, text="Relative* DQI(s): ")
label_amountrel_text.grid(column=0, row=4)
label_amountrel_entry = Entry(window)
label_amountrel_entry.grid(column=1, row=4)

label_infobox_text = Label(window, text="* Specify either an \n absolute or a percentage- \n based rate for DQI")
label_infobox_text.grid(column=0, row=5)


def browse_input_clicked(entry_field):
    filename = filedialog.askopenfilename()
    entry_field.insert(1, filename)


def browse_output_clicked(entry_field):
    filename = filedialog.asksaveasfile()
    entry_field.insert(1, filename.name)


def do_modifications():
    # log manipulation object
    log_obj = LogManipulation()

    # set input and output paths
    log_obj.input_path = label_inputpath_entry.get()
    log_obj.output_path = label_outputpath_entry.get()

    # set amount
    log_obj.relative_amount = float(label_amountrel_entry.get())

    # read input file
    log_obj.read_input_document()

    # read listbox, which issues are selected?
    selected_items = [list_dqis.get(i) for i in list_dqis.curselection()]
    for item in selected_items:
        concat_method_name = "insert_" + item
        method_to_call = getattr(log_obj, concat_method_name)
        method_to_call()

    # write output file again
    log_obj.write_output_document()


# buttons
label_inputpath_button = Button(window, text="Browse", command=partial(browse_input_clicked, label_inputpath_entry))
label_inputpath_button.grid(column=2, row=0)

label_outputpath_button = Button(window, text="Browse", command=partial(browse_output_clicked, label_outputpath_entry))
label_outputpath_button.grid(column=2, row=1)

start_button = Button(window, text="Start", command=do_modifications)
start_button.grid(column=2, row=5)

window.mainloop()
