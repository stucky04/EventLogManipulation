import random
import string
# incorrect case
# pick a random case from other process and insert it at the end of the regarded process
from randomtimestamp import random_date, random_time


def insert_I10(self):
    if self.relative_amount != "":
        # calculate how many cases to insert
        number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
    else:
        number_to_insert = self.absolute_amount

    log_message = "\nMethod insert_I10: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_insert:
        # pick a random case from a different process
        try:
            all_traces_different_process = self.root2.findall(".//trace")
            random_case_different_process = random.choice(all_traces_different_process)
        except:
            print("error selecting random trace")
            continue

        # insert this case at the end of the regarded process
        index_to_insert_at = len(self.root)
        self.root.insert(index_to_insert_at, random_case_different_process)
        log_message = "inserted random case from foreign process at the end of the log " + "\n"
        self.log_documentation = self.log_documentation + log_message

        i = i + 1


# incorrect event
# pick random event from other process and insert it at a random case of the regarded process at random position
def insert_I11(self):
    if self.relative_amount != "":
        # calculate how many cases to insert
        number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
    else:
        number_to_insert = self.absolute_amount

    log_message = "\nMethod insert_I11: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
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
        event_name = self.get_name(random_event_different_process)
        trace_name = self.get_name(random_case)
        log_message = "inserted random event '" + event_name + "' from foreign process in case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message

        i = i + 1


# incorrect relationship
# pick a random event and move to another random trace at a random position
def insert_I12(self):
    if self.relative_amount != "":
        # calculate how many events to move
        number_to_move = int(self.relative_amount * len(self.root.findall(".//event")))
    else:
        number_to_move = self.absolute_amount

    log_message = "\nMethod insert_I12: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_move:
        # pick random event and remove from original trace
        all_events = self.root.findall(".//event")
        random_event = random.choice(all_events)
        event_name = self.get_name(random_event)
        case_name_before = self.get_name(random_event.getparent())
        random_event.getparent().remove(random_event)

        # pick a random other trace and insert there at random position
        all_traces = self.root.findall(".//trace")
        random_trace = random.choice(all_traces)
        case_name_after = self.get_name(random_trace)
        if len(random_trace) <= 3:
            continue
        random_index = random.randrange(3, len(random_trace))
        random_trace.insert(random_index, random_event)
        log_message = "moved event '" + event_name + "' from case " + case_name_before + " to case " + case_name_after + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I13: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_case_attribute = random.choice(self.root.findall(".//trace/"))
        attribute_name = random_case_attribute.get('key')
        case_name = self.get_name(random_case_attribute.getparent())
        if random_case_attribute.tag == 'event':
            continue
        if random_case_attribute.tag == "int":
            random_int = random.choice(range(0, 1000))
            random_case_attribute.set('value', random_int)
        elif random_case_attribute.tag == "string":
            random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
            random_case_attribute.set('value', random_string)
        log_message = "modified attribute '" + attribute_name + "' within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I14: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_of_events_to_modify:
        random_event = random.choice(self.root.findall(".//event"))
        event_name = self.get_name(random_event)
        # move the event to another position within the trace
        trace = random_event.getparent()
        case_name = self.get_name(trace)
        trace.remove(random_event)
        if len(trace) <= 3:
            continue
        random_position_index = random.randrange(3, len(trace))
        trace.insert(random_position_index, random_event)
        log_message = "moved event '" + event_name + "' to another position within the same case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I15: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
        random_event_name = random.choice(self.tree.xpath(".//event/string[@key='concept:name']"))
        case_name = self.get_name(random_event_name.getparent().getparent())
        event_name = random_event_name.get('value')
        random_event_name.set('value', random_string)
        log_message = "modified event name of event '" + event_name + "' within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# incorrect timestamp
# pick random timestamp and change to random value
def insert_I16(self):
    if self.relative_amount != "":
        # calculate how many timestamps to modify
        number_to_modify = int(self.relative_amount * len(self.root.findall(".//date")))
    else:
        number_to_modify = self.absolute_amount

    log_message = "\nMethod insert_I16: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_date_string = str(random_date()) + 'T' + str(random_time()) + '.000+02:00'
        random_date_attribute = random.choice(self.tree.xpath(".//date"))
        # check if timestamp is within an event or trace timestamp
        if random_date_attribute.getparent().tag == 'event':
            case_name = self.get_name(random_date_attribute.getparent().getparent())
        else:
            case_name = self.get_name(random_date_attribute.getparent())
        random_date_attribute.set('value', random_date_string)
        log_message = "modified timestamp to random value within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I17: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_int = random.choice(range(1000))
        random_resource = random.choice(self.tree.xpath(".//event/string[@key='org:resource']"))
        random_resource.set('value', str(random_int))
        event_name = self.get_name(random_resource.getparent())
        case_name = self.get_name(random_resource.getparent().getparent())
        log_message = "modified resource in event '" + event_name + "' within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# incorrect event attribute
# pick random attribute within event and change to random value
def insert_I18(self):  #
    if self.relative_amount != "":
        # calculate how many attributes to modify
        number_to_modify = int(self.relative_amount * len(self.root.findall(".//event/")))
    else:
        number_to_modify = self.absolute_amount

    log_message = "\nMethod insert_I18: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_modify:
        random_event_attribute = random.choice(self.root.findall(".//event/"))
        event_name = self.get_name(random_event_attribute.getparent())
        case_name = self.get_name(random_event_attribute.getparent().getparent())
        if random_event_attribute.get('key') == 'concept:name' or random_event_attribute.get(
                'key') == 'org:resource' or random_event_attribute.get('key') == 'timestamp':
            continue

        if random_event_attribute.tag == float or random_event_attribute.tag == int:
            random_int = random.choice(range(0, 1000))
            random_event_attribute.set('value', random_int)
        elif random_event_attribute.tag == string:
            random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
            random_event_attribute.set('value', random_string)
        log_message = "modified event attribute within event '" + event_name + "' within case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1