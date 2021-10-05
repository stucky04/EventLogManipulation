from tkinter import *
from functools import partial
from tkinter import filedialog
from src.src.functionalities.LogManipulation import *

window = Tk()
window.title("Log Manipulator")
window.geometry('600x400')


# notification method
def popup_message(msg):
    popup = Tk()
    popup.wm_title("Notification")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="OK", command=popup.destroy)
    B1.pack()
    popup.mainloop()


# fields

# input file
label_inputpath_text = Label(window, text="Input Path: ")
label_inputpath_text.grid(column=0, row=0)
label_inputpath_entry = Entry(window, width=60)
label_inputpath_entry.grid(column=1, row=0)

# input file 2 (needed for I10, I11, I26, I27
label_inputpath2_text = Label(window, text="Input Path 2*²: ")
label_inputpath2_text.grid(column=0, row=1)
label_inputpath2_entry = Entry(window, width=60)
label_inputpath2_entry.grid(column=1, row=1)

# output file
label_outputpath_text = Label(window, text="Output Path: ")
label_outputpath_text.grid(column=0, row=2)
label_outputpath_entry = Entry(window, width=60)
label_outputpath_entry.grid(column=1, row=2)

# dqis
label_dqis_text = Label(window, text="DQI(s) to insert: ")
label_dqis_text.grid(column=0, row=3)

list_dqis = Listbox(window, selectmode="multiple", width=60)
list_dqis.grid(column=1, row=3)

# read the dqi description file and load implemented method names and their descriptions into gui
module_names_dict = {}
try:
    description_file_tree = etree.parse("functionalities/dqi/dqi_descriptions")
    description_file_root = description_file_tree.getroot()
    all_dqis = description_file_root.findall(".//dqi")
    for dqi in all_dqis:
        if dqi.get('implemented') == "TRUE":
            concat_name_and_description = dqi.get('name') + "   (" + dqi.get('description_short') + ")"
            list_dqis.insert(END, concat_name_and_description)
            module_names_dict[dqi.get('name')] = dqi.get('module')
except Exception as e:
    popup_message("Some Error reading the DQI description file...")
    print(e)
    exit(1)

yscrollbar = Scrollbar(window)
yscrollbar.grid(column=2, row=3, sticky='NSW')
yscrollbar.config(command=list_dqis.yview)

# amount of dqis
label_amountabs_text = Label(window, text="Absolute* DQI(s): ")
label_amountabs_text.grid(column=0, row=4)
label_amountabs_entry = Entry(window, width=60)
label_amountabs_entry.grid(column=1, row=4)

label_amountrel_text = Label(window, text="Relative* DQI(s) in %: ")
label_amountrel_text.grid(column=0, row=5)
label_amountrel_entry = Spinbox(window, from_=0, to=100, width=58)
label_amountrel_entry.grid(column=1, row=5)

# seed value
label_seed_text = Label(window, text="Seed Value*³: ")
label_seed_text.grid(column=0, row=6)
label_seed_entry = Entry(window, width=60)
label_seed_entry.grid(column=1, row=6)

label_infobox_text = Label(window, text="* specify either an absolute or a percentage-based rate for DQI")
label_infobox_text.grid(column=0, columnspan=2, row=7)

label_infobox_text2 = Label(window,
                            text="*² for I10, I11, I26, I27 a second log file is needed from which \n random cases and events are inserted in the original log")
label_infobox_text2.grid(column=0, columnspan=2, row=9)

label_infobox_text3 = Label(window,
                            text="*³ optional seed value for random operations")
label_infobox_text3.grid(column=0, columnspan=2, row=10)


def browse_input_clicked(entry_field):
    filename = filedialog.askopenfilename()
    entry_field.insert(1, filename)


def browse_output_clicked(entry_field):
    filename = filedialog.asksaveasfile()
    entry_field.insert(1, filename.name)


def do_modifications():
    try:
        # log manipulation object
        log_obj = LogManipulation()

        # set input and output paths
        log_obj.input_path = label_inputpath_entry.get()
        log_obj.output_path = label_outputpath_entry.get()
        log_obj.input_path_to_insert_incorrect_issues = label_inputpath2_entry.get()

        # get amount
        if int(label_amountrel_entry.get()) != 0 and label_amountabs_entry.get() != "":
            popup_message("specify either absolute OR relative amount")

        # set amount
        if int(label_amountrel_entry.get()) != 0:
            log_obj.relative_amount = float(label_amountrel_entry.get()) / 100
        elif label_amountabs_entry.get() != "":
            log_obj.absolute_amount = int(label_amountabs_entry.get())

        # check if seed value given
        if label_seed_entry.get() != "":
            random.seed(label_seed_entry.get())

        # read input file(s)
        log_obj.read_input_document()

        # read listbox, which issues are selected?
        selected_items = [list_dqis.get(i) for i in list_dqis.curselection()]

        # call all needed insert... methods
        for item in selected_items:
            dqi_name = item.split(" ")[0]
            method_call_string = "insert_" + dqi_name
            print(method_call_string)
            module_name = module_names_dict.get(dqi_name)
            method_to_call = getattr(eval(module_name), method_call_string)
            method_to_call(log_obj)

        # write output file again
        log_obj.write_output_document()
        log_obj.create_log_file(log_obj.output_path)

        # add statistics at top of file as a comment
        LogManipulation.add_statistics_to_log(log_obj, log_obj.output_path)
    except Exception as e:
        popup_message("Some Error happened...")
        print(e)
        exit(1)

    # notice user
    popup_message("Modified Log successfully created!")


# buttons
label_inputpath_button = Button(window, text="Browse", command=partial(browse_input_clicked, label_inputpath_entry))
label_inputpath_button.grid(column=2, row=0)

label_inputpath2_button = Button(window, text="Browse", command=partial(browse_input_clicked, label_inputpath2_entry))
label_inputpath2_button.grid(column=2, row=1)

label_outputpath_button = Button(window, text="Browse", command=partial(browse_output_clicked, label_outputpath_entry))
label_outputpath_button.grid(column=2, row=2)

start_button = Button(window, text="Start", command=do_modifications)
start_button.grid(column=2, row=6)

window.mainloop()
