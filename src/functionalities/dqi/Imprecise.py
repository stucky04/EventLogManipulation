import random

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
        print(random_event_name.get('value'))
        random_event_name.set('value', new_event_name)
        print(random_event_name.get('value') + " \n")
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
        if random_timestamp.getparent().tag == 'event':
            case_name = self.get_name(random_timestamp.getparent().getparent())
        else:
            case_name = self.get_name(random_timestamp.getparent())

        timestamp_before = random_timestamp.get('value')
        timestamp_modified = timestamp_before[:7]
        random_timestamp.set('value', timestamp_modified)
        log_message = "modified timestamp within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


def insert_I24(self):
    print("method insert_I24 not implemented because not applicable")
    return


def insert_I25(self):
    print("method insert_I25 not implemented because not applicable")
    return