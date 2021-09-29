import random


# missing cases
# randomly deletes specified amount of cases
def insert_I1(self):
    if self.relative_amount != 0:
        # calculate how many cases to remove
        number_of_cases_to_remove = int(
            self.relative_amount * len(self.root.findall(".//trace")))
    else:
        number_of_cases_to_remove = self.absolute_amount

    log_message = "\nMethod insert_I1: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_of_cases_to_remove:
        random_case = random.choice(self.root.findall(".//trace"))
        random_case_name = self.get_name(random_case)

        random_case.getparent().remove(random_case)
        log_message = "removed case with name " + random_case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I2: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_of_events_to_remove:
        random_event = random.choice(self.root.findall(".//event"))
        random_event_name = self.get_name(random_event)
        random_case_name = self.get_name(random_event.getparent())
        random_event.getparent().remove(random_event)
        log_message = "removed event '" + random_event_name + "' from case " + random_case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I3: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_of_case_attributes_to_remove:
        random_child = random.choice(all_trace_children)
        if random_child.tag == 'event' or random_child.getparent() is None:
            continue

        random_case_name = self.get_name(random_child.getparent())

        random_child.getparent().remove(random_child)
        log_message = "removed attribute '" + random_child.get('key') + "' from case " + random_case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# missing position
# pick random events and delete their timestamp, then move them to other traces at a random position
def insert_I5(self):
    if self.relative_amount != "":
        # calculate how many events to modify
        number_of_events_to_modify = int(
            self.relative_amount * len(self.root.findall(".//event")))
    else:
        number_of_events_to_modify = self.absolute_amount

    log_message = "\nMethod insert_I5: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_of_events_to_modify:
        random_event = random.choice(self.root.findall(".//event"))
        # delete timestamp of random event
        random_event_name = self.get_name(random_event)
        for attribute in random_event:
            if attribute.tag == 'date':
                random_event.remove(attribute)

        # move the event to another position within the trace
        trace = random_event.getparent()
        trace.remove(random_event)

        trace_name = self.get_name(trace)

        if len(trace) <= 3:
            continue
        random_position_index = random.randrange(3, len(trace))
        trace.insert(random_position_index, random_event)
        log_message = "removed timestamp and moved event '" + random_event_name + "' within case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I6: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_delete:
        random_event_name = random.choice(self.tree.xpath(".//event/string[@key='concept:name']"))
        event = random_event_name.getparent()
        trace_name = self.get_name(event.getparent())

        random_event_name.getparent().remove(random_event_name)
        log_message = "removed event name of event '" + random_event_name.get(
            'value') + "' within case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# missing timestamps
# randomly pick events and delte their timestamp
def insert_I7(self):
    if self.relative_amount != "":
        # calculate how many activity names to modify
        number_to_delete = int(self.relative_amount * len(self.root.findall(".//event/date")))
    else:
        number_to_delete = self.absolute_amount

    log_message = "\nMethod insert_I7: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_delete:
        random_event_timestamp = random.choice(self.tree.xpath(".//event/date"))
        event = random_event_timestamp.getparent()
        trace_name = self.get_name(event.getparent())
        event_name = self.get_name(event)
        random_event_timestamp.getparent().remove(random_event_timestamp)
        log_message = "removed timestamp of event '" + event_name + "' within case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message
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

    log_message = "\nMethod insert_I8: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_delete:
        random_event_name = random.choice(self.tree.xpath(".//event/string[@key='org:resource']"))
        event = random_event_name.getparent()
        event_name = self.get_name(event)
        trace_name = self.get_name(event.getparent())
        random_event_name.getparent().remove(random_event_name)
        log_message = "removed resource attribute of event '" + event_name + "' within case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# missing event attributes
# pick random event attributes and delete them
def insert_I9(self):
    if self.relative_amount != "":
        # calculate how many activity names to modify
        number_to_delete = int(self.relative_amount * len(self.root.findall(".//event/")))
    else:
        number_to_delete = self.absolute_amount

    log_message = "\nMethod insert_I9: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_delete:
        random_event_attribute = random.choice(self.root.findall(".//event/"))
        event = random_event_attribute.getparent()
        event_attribute_name = self.get_name(random_event_attribute)
        event_name = self.get_name(event)
        trace_name = self.get_name(event.getparent())
        random_event_attribute.getparent().remove(random_event_attribute)
        log_message = "removed event attribute '" + event_attribute_name + "' of event '" + event_name + "' within case " + trace_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1