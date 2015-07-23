

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
            callers_str = callers_str + c.name + ", "
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
    def __init__(self, name, location="Bay Area"):
        self.name = name
        self.location = location

    def __str__(self):
        return self.name

def get_person_name_location(s):
    if "[" not in s:
        return s, "Bay Area"

    (name, loc) = s.split("[")
    return name.strip(), loc.strip()[:-1].strip()
        
def parse_file(filename):
    dances = []
    lines = open(filename).readlines()

    for l in lines:
        (date, dance_location, callers, band_info) = l.split(",", 3)

        callers_list = []
        for c in callers.split("and"):
            (caller_name, caller_location) = get_person_name_location(c)
            callers_list.append(Person(caller_name, caller_location))

        (band_name, band_members) = band_info.split("(")
        band_members_list = []
        for m in band_members.strip()[:-1].split(","):
            (name, location) = get_person_name_location(m)
            band_members_list.append(Person(name=name, location=location))
        
        dances.append(Dance(
            date = date.strip(), # TODO: make an actual datetime
            location = dance_location.strip(),
            band = Band(
                name = band_name.strip(),
                members = band_members_list
            ),
            callers = callers_list
        ))
    
    return dances

if __name__ == "__main__":
    filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    dances = parse_file(filename)
    for d in dances:
        print(d)
        
