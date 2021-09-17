import os
import random
import string
import statistics
from lxml import etree
from randomtimestamp import random_time, random_date


class LogManipulation:
    input_path = ""
    input_path_to_insert_incorrect_issues = ""
    output_path = ""
    relative_amount = 0
    absolute_amount = 0
    number_of_case_attributes_per_case = 3

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

    # missing cases
    # randomly deletes specified amount of cases
    def insert_I1(self):
        if self.relative_amount != 0:
            # calculate how many cases to remove
            number_of_cases_to_remove = int(
                self.relative_amount * len(self.root.findall(".//trace")))
        else:
            number_of_cases_to_remove = self.absolute_amount

        i = 0
        while i < number_of_cases_to_remove:
            random_case = random.choice(self.root.findall(".//trace"))
            # try:
            #     for child_node in random_case.getchildren():
            #         if child_node.get('key') == 'concept:name':
            #             print("...method insert_I1 ... removing case with name ... " + child_node.get('value'))
            # except:
            #     print("error writing console log")
            random_case.getparent().remove(random_case)
            i = i + 1

    # missing events
    # randomly delete specified amount of events
    def insert_I2(self):
        if self.relative_amount != 0:
            # calculate how many events to remove
            number_of_events_to_remove = int(
                self.relative_amount * len(self.root.findall(".//event")))
        else:
            number_of_events_to_remove = self.absolute_amount

        i = 0
        while i < number_of_events_to_remove:
            random_event = random.choice(self.root.findall(".//event"))
            # try:
            #     for child_node in random_event.getchildren():
            #         if child_node.get('key') == 'concept:name':
            #             print("...method insert_I2 ... removing event with name ... " + child_node.get(
            #                 'value') + " ... from case with name ... " + random_event.getparent().getchildren()[0].get(
            #                 'value'))
            # except:
            #     print("error writing console log")

            random_event.getparent().remove(random_event)
            i = i + 1

    # missing relationships
    def insert_I3(self):
        print("method insert_I3 not implemented because not applicable")

    # missing case attributes
    # randomly delete case attributes
    def insert_I4(self):
        all_trace_children = self.root.findall(".//trace/")
        number_of_case_attributes = 0
        for element in all_trace_children:
            if element.tag != 'event':
                number_of_case_attributes = number_of_case_attributes + 1

        if self.relative_amount != "":
            # calculate how many to remove
            number_of_case_attributes_to_remove = int(self.relative_amount * number_of_case_attributes)
        else:
            number_of_case_attributes_to_remove = int(self.absolute_amount)

        i = 0
        while i < number_of_case_attributes_to_remove:
            random_child = random.choice(all_trace_children)
            if random_child.tag == 'event':
                continue
            # try:
            #     print("...method insert_I4 ... removing case attribute ... " + random_child.get(
            #         'key') + " ... from case with name ... " + random_child.getparent().getchildren()[
            #               0].get(
            #         'value'))
            # except:
            #     print("error writing console log")
            try:
                random_child.getparent().remove(random_child)
                i = i + 1
            except AttributeError:
                print("error removing case attribute")

    # missing position
    # pick random events and delete their timestamp, then move them to other traces at a random position
    def insert_I5(self):
        if self.relative_amount != "":
            # calculate how many events to modify
            number_of_events_to_modify = int(
                self.relative_amount * len(self.root.findall(".//event")))
        else:
            number_of_events_to_modify = self.absolute_amount

        i = 0
        while i < number_of_events_to_modify:
            random_event = random.choice(self.root.findall(".//event"))
            # delete timestamp of random event
            for attribute in random_event:
                if attribute.tag == 'date':
                    random_event.remove(attribute)

            # move the event to another position within the trace
            trace = random_event.getparent()
            trace.remove(random_event)
            # print("Trace Length: " + str(len(trace)))
            # print(etree.tostring(trace, pretty_print=True).decode())
            if len(trace) <= 3:
                continue
            random_position_index = random.randrange(3, len(trace))
            trace.insert(random_position_index, random_event)
            i = i + 1

    # missing activity names
    # randomly delete specified amount of activity names
    def insert_I6(self):
        if self.relative_amount != "":
            # calculate how many activity names to modify
            number_to_delete = int(
                self.relative_amount * len(self.root.findall(".//event/string[@key='concept:name']")))
        else:
            number_to_delete = self.absolute_amount

        i = 0
        while i < number_to_delete:
            random_event_name = random.choice(self.tree.xpath(".//event/string[@key='concept:name']"))
            event = random_event_name.getparent()
            random_event_name.getparent().remove(random_event_name)
            i = i + 1

    # missing timestamps
    # randomly pick events and delte their timestamp
    def insert_I7(self):
        if self.relative_amount != "":
            # calculate how many activity names to modify
            number_to_delete = int(self.relative_amount * len(self.root.findall(".//event/date")))
        else:
            number_to_delete = self.absolute_amount

        i = 0
        while i < number_to_delete:
            random_event_timestamp = random.choice(self.tree.xpath(".//event/date"))
            event = random_event_timestamp.getparent()
            random_event_timestamp.getparent().remove(random_event_timestamp)
            i = i + 1

    # missing resource
    # pick random 'org:resource' tags and delete them
    def insert_I8(self):
        if self.relative_amount != "":
            # calculate how many activity names to modify
            number_to_delete = int(
                self.relative_amount * len(self.root.findall(".//event/string[@key='org:resource']")))
        else:
            number_to_delete = self.absolute_amount

        i = 0
        while i < number_to_delete:
            random_event_name = random.choice(self.tree.xpath(".//event/string[@key='org:resource']"))
            event = random_event_name.getparent()
            random_event_name.getparent().remove(random_event_name)
            i = i + 1

    # missing event attributes
    # pick random event attributes and delete them
    def insert_I9(self):
        if self.relative_amount != "":
            # calculate how many activity names to modify
            number_to_delete = int(self.relative_amount * len(self.root.findall(".//event/")))
        else:
            number_to_delete = self.absolute_amount

        i = 0
        while i < number_to_delete:
            random_event_attribute = random.choice(self.root.findall(".//event/"))
            event = random_event_attribute.getparent()
            random_event_attribute.getparent().remove(random_event_attribute)
            i = i + 1

    # incorrect case
    # pick a random case from other process and insert it at the end of the regarded process
    def insert_I10(self):
        if self.relative_amount != "":
            # calculate how many cases to insert
            number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
        else:
            number_to_insert = self.absolute_amount

        i = 0
        while i < number_to_insert:
            # pick a random case from a different process
            try:
                all_traces_different_process = self.root2.findall(".//trace")
                random_case_different_process = random.choice(all_traces_different_process)
                print("random choice successful " + str(i))
            except:
                print("error selecting random trace")
                continue

            # insert this case at the end of the regarded process
            index_to_insert_at = len(self.root)
            self.root.insert(index_to_insert_at, random_case_different_process)

            i = i + 1

    # incorrect event
    # pick random event from other process and insert it at a random case of the regarded process at random position
    def insert_I11(self):
        if self.relative_amount != "":
            # calculate how many cases to insert
            number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
        else:
            number_to_insert = self.absolute_amount

        i = 0
        while i < number_to_insert:
            # pick a random event from a different process
            try:
                all_events_different_process = self.root2.findall(".//event")
                random_event_different_process = random.choice(all_events_different_process)
            except:
                continue

            # pick a random case of original process and insert event at a random position
            all_cases = self.root.findall(".//trace")
            random_case = random.choice(all_cases)
            if len(random_case) <= 3:
                continue
            random_index = random.randrange(3, len(random_case))
            random_case.insert(random_index, random_event_different_process)

            i = i + 1

    # incorrect relationship
    # pick a random event and move to another random trace at a random position
    def insert_I12(self):
        if self.relative_amount != "":
            # calculate how many events to move
            number_to_move = int(self.relative_amount * len(self.root.findall(".//event")))
        else:
            number_to_move = self.absolute_amount

        i = 0
        while i < number_to_move:
            # pick random event and remove from original trace
            all_events = self.root.findall(".//event")
            random_event = random.choice(all_events)
            random_event.getparent().remove(random_event)

            # pick a random other trace and insert there at random position
            all_traces = self.root.findall(".//trace")
            random_trace = random.choice(all_traces)
            if len(random_trace) <= 3:
                continue
            random_index = random.randrange(3, len(random_trace))
            random_trace.insert(random_index, random_event)

            i = i + 1

    # incorrect case attribute
    # pick a random case attribute and change to random value
    # case attributes: concept:name, variant:count, variant:index
    def insert_I13(self):
        if self.relative_amount != "":
            # calculate how many attributes to modify
            number_to_modify = int(
                self.relative_amount * len(self.root.findall(".//trace")) * self.number_of_case_attributes_per_case)
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_case_attribute = random.choice(self.root.findall(".//trace/"))
            if random_case_attribute.tag == 'event':
                continue
            if random_case_attribute.tag == int:
                random_int = random.choice(range(0, 1000))
                random_case_attribute.set('value', random_int)
            elif random_case_attribute.tag == string:
                random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
                random_case_attribute.set('value', random_string)
            i = i + 1

    # incorrect position
    # pick event within a trace and move to other position within the SAME trace
    def insert_I14(self):
        if self.relative_amount != "":
            # calculate how many events to modify
            number_of_events_to_modify = int(
                self.relative_amount * len(self.root.findall(".//event")))
        else:
            number_of_events_to_modify = self.absolute_amount

        i = 0
        while i < number_of_events_to_modify:
            random_event = random.choice(self.root.findall(".//event"))

            # move the event to another position within the trace
            trace = random_event.getparent()
            trace.remove(random_event)
            if len(trace) <= 3:
                continue
            random_position_index = random.randrange(3, len(trace))
            trace.insert(random_position_index, random_event)

            i = i + 1

    # incorrect activity name
    # pick random event and set activity name to random string value
    def insert_I15(self):
        if self.relative_amount != "":
            # calculate how many activity names to modify
            number_to_modify = int(
                self.relative_amount * len(self.root.findall(".//event/string[@key='concept:name']")))
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
            random_event_name = random.choice(self.tree.xpath(".//event/string[@key='concept:name']"))
            random_event_name.set('value', random_string)
            i = i + 1

    # incorrect timestamp
    # pick random timestamp and change to random value
    def insert_I16(self):
        if self.relative_amount != "":
            # calculate how many timestamps to modify
            number_to_modify = int(self.relative_amount * len(self.root.findall(".//date")))
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_date_string = str(random_date()) + 'T' + str(random_time()) + '.000+02:00'
            random_date_attribute = random.choice(self.tree.xpath(".//date"))
            random_date_attribute.set('value', random_date_string)
            i = i + 1

    # incorrect resource
    # pick random org:resource and change to random value
    def insert_I17(self):
        if self.relative_amount != "":
            # calculate how many resources to modify
            number_to_modify = int(
                self.relative_amount * len(self.root.findall(".//event/string[@key='org:resource']")))
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_int = random.choice(range(1000))
            random_resource = random.choice(self.tree.xpath(".//event/string[@key='org:resource']"))
            random_resource.set('value', str(random_int))
            i = i + 1

    # incorrect event attribute
    # pick random attribute within event and change to random value
    def insert_I18(self):  #
        if self.relative_amount != "":
            # calculate how many attributes to modify
            number_to_modify = int(self.relative_amount * len(self.root.findall(".//event/")))
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_event_attribute = random.choice(self.root.findall(".//event/"))
            if random_event_attribute.get('key') == 'concept:name' or random_event_attribute.get(
                    'key') == 'org:resource' or random_event_attribute.get('key') == 'timestamp':
                continue

            if random_event_attribute.tag == float or random_event_attribute.tag == int:
                random_int = random.choice(range(0, 1000))
                random_event_attribute.set('value', random_int)
            elif random_event_attribute.tag == string:
                random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
                random_event_attribute.set('value', random_string)
            i = i + 1

    def insert_I19(self):
        print("method insert_I19 not implemented because not applicable")

    def insert_I20(self):
        print("method insert_I20 not implemented because not applicable")
        return

    def insert_I21(self):
        print("method insert_I21 not implemented because not applicable")
        return

    def insert_I22(self):
        print("method insert_I22 not implemented because not applicable")
        return

    # imprecise timestamp
    # pick random timestamp and cut off time and day of the
    def insert_I23(self):
        if self.relative_amount != "":
            # calculate how many timestamps to modify
            number_to_modify = int(self.relative_amount * len(self.root.findall(".//date")))
        else:
            number_to_modify = self.absolute_amount

        i = 0
        while i < number_to_modify:
            random_timestamp = random.choice(self.tree.xpath(".//date"))
            timestamp_before = random_timestamp.get('value')
            timestamp_modified = timestamp_before[:7]
            random_timestamp.set('value', timestamp_modified)
            i = i + 1

    def insert_I24(self):
        print("method insert_I24 not implemented because not applicable")
        return

    def insert_I25(self):
        print("method insert_I25 not implemented because not applicable")
        return

    # imprecise case
    def insert_I26(self):
        if self.relative_amount != "":
            # calculate how many cases to insert
            number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
        else:
            number_to_insert = self.absolute_amount

        i = 0
        while i < number_to_insert:
            # pick a random case from a different process
            all_traces_different_process = self.root2.findall(".//trace")
            random_case_different_process = random.choice(all_traces_different_process)

            # insert this case at the end of the regarded process
            index_to_insert_at = len(self.root)
            self.root.insert(index_to_insert_at, random_case_different_process)

            i = i + 1

    # imprecise event
    def insert_I27(self):
        if self.relative_amount != "":
            # calculate how many events to insert
            number_to_insert = int(self.relative_amount * len(self.root.findall(".//event")))
        else:
            number_to_insert = self.absolute_amount

        i = 0
        while i < number_to_insert:
            # pick a random event from a different process
            try:
                all_events_different_process = self.root2.findall(".//event")
                random_event_different_process = random.choice(all_events_different_process)
            except:
                continue

            # pick a random case of original process and insert event at a random position
            all_cases = self.root.findall(".//trace")
            random_case = random.choice(all_cases)
            if len(random_case) <= 3:
                continue
            random_index = random.randrange(3, len(random_case))
            random_case.insert(random_index, random_event_different_process)
            print("inserted " + str(i))
            i = i + 1

    # method adds all statistics at the top of given document as a comment
    def add_statistics_to_log(path):
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


def generate_all_logs():
    relative_amounts = ["0.05", "0.10", "0.15"]
    implemented_methods = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23,
                           26, 27]
    implemented_methods = [23,
                           26, 27]

    log_obj = LogManipulation()
    log_obj.tree2 = etree.parse("../EventLogsIn/Hospital_Billing_Full.xes")
    log_obj.root2 = log_obj.tree2.getroot()

    random.seed(1)

    for issue in implemented_methods:
        log_obj.tree = etree.parse("../EventLogsIn/03_RTF_Log_Initial_Filtered_Sample10000_DefaultDelays0.xes")
        log_obj.root = log_obj.tree.getroot()
        for percentage in relative_amounts:
            log_obj.relative_amount = float(percentage)

            method_call_string = "insert_I" + str(issue)
            print(method_call_string)
            method_to_call = getattr(log_obj, method_call_string)
            method_to_call()
            file_name_string = "../EventLogsOut/" + "i" + str(issue) + "_" + percentage[2:] + "percent.xes"
            print(file_name_string)
            log_obj.output_path = file_name_string
            log_obj.write_output_document()


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


if __name__ == '__main__':
    print("test")
