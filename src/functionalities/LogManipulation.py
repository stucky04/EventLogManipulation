import os
import random
import statistics
from lxml import etree

# import modules
import src.src.functionalities.dqi.Missing as Missing
import src.src.functionalities.dqi.Irrelevant as Irrelevant
import src.src.functionalities.dqi.Imprecise as Imprecise
import src.src.functionalities.dqi.Incorrect as Incorrect


class LogManipulation:
    input_path = ""
    input_path_to_insert_incorrect_issues = ""
    output_path = ""
    relative_amount = 0
    absolute_amount = 0
    number_of_case_attributes_per_case = 3
    log_documentation = "Log Manipulation Documentation \n"

    tree = None
    root = None
    tree2 = None
    root2 = None

    # read input file
    def read_input_document(self):
        # use these for lxml operations
        self.tree = etree.parse(self.input_path)
        self.root = self.tree.getroot()
        # for random insertion: a second log from which cases and events are picked and inserted
        self.tree2 = etree.parse(self.input_path_to_insert_incorrect_issues)
        self.root2 = self.tree2.getroot()

    # write tree to log file again
    def write_output_document(self):
        # write resulting log to document
        self.tree.write(self.output_path, pretty_print=True)

    # method to get name of an event or case
    def get_name(self, node):
        for attribute in node:
            if attribute.get('key') == 'concept:name':
                return attribute.get('value')
        return ""

    # method adds all statistics at the top of given document as a comment
    def add_statistics_to_log(self, path):
        log = etree.parse(path)
        root = log.getroot()

        all_events = root.findall(".//event")
        number_of_events = len(all_events)

        all_traces = root.findall(".//trace")
        number_of_cases = len(all_traces)

        all_trace_lengths = []
        for case in all_traces:
            all_trace_lengths.append(len(case.getchildren()) - 3)
        avg_trace_length = statistics.mean(all_trace_lengths)

        all_case_attributes = []
        for case in all_traces:
            for case_attribute in case:
                if case_attribute.tag != "event":
                    concat = case_attribute.tag + ": " + case_attribute.get('key')
                    if concat not in all_case_attributes:
                        all_case_attributes.append(concat)
        list_of_case_attributes = all_case_attributes

        all_event_attributes = []
        for event in all_events:
            for event_attribute in event:
                concat = event_attribute.tag + ": " + event_attribute.get('key')
                if concat not in all_event_attributes:
                    all_event_attributes.append(concat)
        list_of_event_attributes = all_event_attributes

        root.addprevious(etree.Comment("Statistics calculated by Log Manipulator: \n" +
                                       "    number of cases: " + str(number_of_cases) + "\n" +
                                       "    number of events: " + str(number_of_events) + "\n" +
                                       "    average trace length: " + str(avg_trace_length) + "\n" +
                                       "    used case attributes: " + str(list_of_case_attributes) + "\n" +
                                       "    used event attributes: " + str(list_of_event_attributes) + "\n"))
        log.write(path, pretty_print=True)

    def create_log_file(self, path):
        edited_path = path + "LOG_FILE.txt"
        f = open(edited_path, "w")
        f.write(self.log_documentation)
        f.close()
        self.log_documentation = ""

    def remove_delay(self, delay_x, trace_node, trace_name):
        for event in trace_node:
            for attribute in event:
                if attribute.get('key') == delay_x:
                    event.remove(attribute)
                    log_message = "removed " + delay_x + " from case " + trace_name + " \n"
                    self.log_documentation = self.log_documentation + log_message


def generate_all_logs():
    relative_amounts = ["0.05", "0.10", "0.15"]
    implemented_methods = [1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23,
                           26]

    # for specific logs only TODO I9, I18, I27 very time-consuming, "event attribute" operations
    implemented_methods = [27]
    # relative_amounts = ["0.05"]

    log_obj = LogManipulation()
    log_obj.tree2 = etree.parse("../EventLogsIn/Hospital_Billing_Full.xes")
    log_obj.root2 = log_obj.tree2.getroot()

    random.seed(1)

    for issue in implemented_methods:
        for percentage in relative_amounts:
            # log_obj.tree = etree.parse("../Logs_Alizadeh_Sample20/Fit1_Sample20.xes")
            log_obj.tree = etree.parse("../EventLogsIn/03_RTF_Log_Initial_Filtered_Sample10000_DefaultDelays0.xes")
            log_obj.root = log_obj.tree.getroot()
            log_obj.relative_amount = float(percentage)
            method_call_string = "insert_I" + str(issue)
            if issue in range(1, 10):
                method_to_call = getattr(Missing, method_call_string)
            elif issue in range(10, 19):
                method_to_call = getattr(Incorrect, method_call_string)
            elif issue in range(19, 26):
                method_to_call = getattr(Imprecise, method_call_string)
            else:
                method_to_call = getattr(Irrelevant, method_call_string)

            print(method_call_string)
            method_to_call(log_obj)
            file_name_string = "../TestDir/" + "i" + str(issue) + "_" + percentage[2:] + "percent.xes"
            log_file_name_string = "../TestDir/" + "i" + str(issue) + "_" + percentage[2:] + "percent"
            print(file_name_string)
            log_obj.output_path = file_name_string
            log_obj.write_output_document()
            log_obj.create_log_file(log_file_name_string)


def change_default_delay_values():
    directory = "../EventLogsOut"
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        tree = etree.parse(path)
        root = tree.getroot()
        all_delay_send_attributes = root.findall(".//event/float[@key='delay_send']")
        all_delay_judge_attributes = root.findall(".//event/float[@key='delay_judge']")
        all_delay_prefecture_attributes = root.findall(".//event/float[@key='delay_prefecture']")

        for attribute in all_delay_send_attributes:
            if float(attribute.get('value')) == -99.0:
                attribute.set('value', '0.0')

        for attribute in all_delay_judge_attributes:
            if float(attribute.get('value')) == -99.0:
                attribute.set('value', '0.0')

        for attribute in all_delay_prefecture_attributes:
            if float(attribute.get('value')) == -99.0:
                attribute.set('value', '0.0')

        new_path = "../EventLogsOutDefaultDelay0/" + filename
        tree.write(new_path, pretty_print=True)


def sample_x_distinct_traces(x):
    log_obj = LogManipulation()
    log_obj.tree = etree.parse("../EventLogsIn/03_RTF_Log_Initial_Filtered_Sample10000_DefaultDelays0.xes")
    log_obj.root = log_obj.tree.getroot()
    all_traces = log_obj.root.findall(".//trace")
    all_traces_list = []
    trace_id_list = []
    for trace in all_traces:
        single_event_list = []
        trace_id = log_obj.get_name(trace)
        for event in trace:
            event_name = log_obj.get_name(event)
            single_event_list.append(event_name)
        if not single_event_list in all_traces_list and len(all_traces_list) < 20:
            all_traces_list.append(single_event_list)
            trace_id_list.append(trace_id)

    for trace in all_traces:
        if log_obj.get_name(trace) not in trace_id_list:
            log_obj.root.remove(trace)

    print(all_traces_list)
    print(len(all_traces_list))
    print(trace_id_list)
    log_obj.tree.write("sample.xes", pretty_print=True)


if __name__ == '__main__':
    # log_obj = LogManipulation()
    # directory = os.listdir("../TestDir")
    # for filename in directory:
    #     if not filename.__contains__("LOG_FILE"):
    #         #print(str(os.path.join(directory, filename)))
    #         log_obj.add_statistics_to_log(os.path.join("../TestDir/", filename))
    #         #print(filename)
    path = "../TestDir/i15_10percent.xes"
    log_obj = LogManipulation()
    log_obj.tree = etree.parse(path)
    log_obj.root = log_obj.tree.getroot()
    all_traces = log_obj.root.findall(".//trace")
    for trace in all_traces:
        if len(trace.getchildren()) > 20:
            print("Trace: " + log_obj.get_name(trace) + " Length: " + str(len(trace.getchildren())))

