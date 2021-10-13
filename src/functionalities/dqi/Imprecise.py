import random
import src.src.functionalities.LogManipulation


def insert_I19(self):
    print("method insert_I19 not implemented because not applicable")


def insert_I20(self):
    print("method insert_I20 not implemented because not applicable")
    return

    # imprecise position
    # pick a random trace and delete the timestamp of all events within


def insert_I21(self):
    if self.relative_amount != "":
        # calculate how many traces to modify
        number_to_modify = int(self.relative_amount * len(self.root.findall(".//trace")))
    else:
        number_to_modify = self.absolute_amount

    log_message = "\nMethod insert_I21: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_case = random.choice(self.root.findall(".//trace"))
        case_name = self.get_name(random_case)
        for event in random_case.getchildren():
            for attribute in event.getchildren():
                if attribute.get('key') == 'time:timestamp':
                    event.remove(attribute)
        log_message = "removed timestamps of events within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message

        self.remove_delay("delay_send", random_case, case_name)
        self.remove_delay("delay_judge", random_case, case_name)
        self.remove_delay("delay_prefecture", random_case, case_name)

        i = i + 1

    # imprecise activity name
    # pick random activity name, split string at " " and use only first word


def insert_I22(self):
    if self.relative_amount != "":
        # calculate how many activity names to modify
        number_to_delete = int(
            self.relative_amount * len(self.root.findall(".//event/string[@key='concept:name']")))
    else:
        number_to_delete = self.absolute_amount

    log_message = "\nMethod insert_I22: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_delete:
        random_event_name = random.choice(self.tree.xpath(".//event/string[@key='concept:name']"))
        event_name = self.get_name(random_event_name.getparent())
        case_name = self.get_name(random_event_name.getparent().getparent())
        old_event_name = random_event_name.get('value')
        new_event_name = old_event_name.split(" ")[0]
        random_event_name.set('value', new_event_name)
        log_message = "modified event name of event '" + event_name + "' within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# imprecise timestamp
# pick random timestamp and cut off time and day of the timestamp string
def insert_I23(self):
    if self.relative_amount != "":
        # calculate how many timestamps to modify
        number_to_modify = int(self.relative_amount * len(self.root.findall(".//date")))
    else:
        number_to_modify = self.absolute_amount

    log_message = "\nMethod insert_I23: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_timestamp = random.choice(self.tree.xpath(".//date"))
        # check if timestamp is within an event or trace timestamp
        event_node = None
        if random_timestamp.getparent().tag == 'event':
            case_name = self.get_name(random_timestamp.getparent().getparent())
            event_node = random_timestamp.getparent()
        else:
            case_name = self.get_name(random_timestamp.getparent())

        timestamp_before = random_timestamp.get('value')
        timestamp_modified = timestamp_before[:7]
        random_timestamp.set('value', timestamp_modified)
        log_message = "modified timestamp within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message

        if event_node is not None:
            event_name = self.get_name(event_node)
            if event_name == "Create Fine" or event_name == "Send Fine":
                # remove delay_send from Create_Fine
                self.remove_delay("delay_send", event_node.getparent(), case_name)
            elif event_name == "Insert Fine Notification" or event_name == "Appeal to Judge":
                # remove delay_judge from Insert Fine Notification
                self.remove_delay("delay_judge", event_node.getparent(), case_name)
            elif event_name == "Insert Fine Notification" or event_name == "Insert Date Appeal to Prefecture":
                # remove delay_prefecture from Insert Fine Notification
                self.remove_delay("delay_prefecture", event_node.getparent(), case_name)

        i = i + 1


def insert_I24(self):
    print("method insert_I24 not implemented because not applicable")
    return


def insert_I25(self):
    print("method insert_I25 not implemented because not applicable")
    return
