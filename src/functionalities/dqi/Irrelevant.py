import random
# irrelevant case
def insert_I26(self):
    if self.relative_amount != "":
        # calculate how many cases to insert
        number_to_insert = int(self.relative_amount * len(self.root.findall(".//trace")))
    else:
        number_to_insert = self.absolute_amount

    log_message = "\nMethod insert_I26: \n----------------------------------------------------------------------------\n"
    self.log_documentation = self.log_documentation + log_message
    i = 0
    while i < number_to_insert:
        # pick a random case from a different process
        all_traces_different_process = self.root2.findall(".//trace")
        random_case_different_process = random.choice(all_traces_different_process)

        # insert this case at the end of the regarded process
        index_to_insert_at = len(self.root)
        self.root.insert(index_to_insert_at, random_case_different_process)

        log_message = "inserted random case from foreign process at the end of the log \n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1


# irrelevant event
def insert_I27(self):
    if self.relative_amount != "":
        # calculate how many events to insert
        number_to_insert = int(self.relative_amount * len(self.root.findall(".//event")))
    else:
        number_to_insert = self.absolute_amount

    log_message = "\nMethod insert_I27: \n----------------------------------------------------------------------------\n"
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
        case_name = self.get_name(random_case)
        if len(random_case) <= 3:
            continue
        random_index = random.randrange(3, len(random_case))
        random_case.insert(random_index, random_event_different_process)
        log_message = "inserted random event from foreign process in case " + case_name + "\n"
        self.log_documentation = self.log_documentation + log_message
        i = i + 1