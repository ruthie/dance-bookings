from datetime import date
from collections import OrderedDict

class Dance():
    def __init__(self, date, location, band, callers):
        self.date = date
        self.location = location
        self.band = band
        self.callers = callers

    def __str__(self):
        # TODO: must be a nicer way to do this
        callers_str = ""
        for c in self.callers:
            callers_str = callers_str + str(c) + ", "
        callers_str = callers_str[:-2]
        
        return "{self.date}, {self.location}, {self.band}, {callers_str}".format(**locals())

class Band():
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __str__(self):
        s = self.name + " ("
        # TODO: should be able to accumulate here
        for m in self.members:
            s = s + str(m) + ", "
        s = s[:-2] + ")"
        return s

class Person():
    def __init__(self, name, location):
        self.name = name
        if location is None:
            location = "Bay Area"
        self.location = location

    def __str__(self):
        return self.name + "/" + self.location

def get_name_location(s):
    if "[" not in s:
        return s.strip(), None

    (name, loc) = s.split("[")
    return name.strip(), loc.strip()[:-1].strip()

def date_from_string(s):
    (month, day, year) = s.strip().split("/")
    return date(month=int(month), day=int(day), year=int(year))

def parse_file(filename):
    dances = []
    lines = open(filename).readlines()

    for l in lines:
        (dance_date, dance_location, callers, band_info) = l.split(",", 3)

        # caller info
        callers_list = []
        for c in callers.split(" and "):
            (caller_name, caller_location) = get_name_location(c)
            callers_list.append(Person(caller_name, caller_location))

        # band info
        (band_name, band_members) = band_info.split("(")
        band_members_list = []
        (band_name, band_location) = get_name_location(band_name)
        
        for m in band_members.strip()[:-1].split(","):
            (member_name, member_location) = get_name_location(m)
            if member_location is None:
                member_location = band_location
            band_members_list.append(Person(name=member_name, location=member_location))

        # actually create the band
        dances.append(Dance(
            date = date_from_string(dance_date),
            location = dance_location.strip(),
            band = Band(
                name = band_name.strip(),
                members = band_members_list
            ),
            callers = callers_list
        ))
    
    return dances

def get_most_booked_musicians(dances):
    return frequency_dict(dances, lambda x: x.band.members)

def get_most_booked_callers(dances):
    return frequency_dict(dances, lambda x: x.callers)

def frequency_dict(dances, getter):
    items = {}
    for d in dances:
        dance_items = getter(d)
        for i in dance_items:
            if i.name not in items:
                items[i.name] = 0
            items[i.name] = items[i.name] + 1

    return items

def print_dict_alphabetical(d):
    for k in sorted(d.keys()):
        print("{}: {}".format(k, d[k]))

def print_dict_value_ordered(d):
    # TODO: bla how sholud I actually do this?
    tuples = [(k, d[k]) for k in d.keys()]
    tuples.sort(key=lambda x: x[1], reverse=True)
    od = OrderedDict(tuples)

    for k in od:
        print("{}: {}".format(k, od[k]))
        
if __name__ == "__main__":
    filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    dances = parse_file(filename)
    callers = get_most_booked_callers(dances)
    print_dict_value_ordered(callers)
