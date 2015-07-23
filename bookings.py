from datetime import date

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
        for c in callers.split("and"):
            (caller_name, caller_location) = get_person_name_location(c)
            callers_list.append(Person(caller_name, caller_location))

        # band info
        (band_name, band_members) = band_info.split("(")
        band_members_list = []
        # TODO: carry over band location to musicians
        for m in band_members.strip()[:-1].split(","):
            (name, location) = get_person_name_location(m)
            band_members_list.append(Person(name=name, location=location))

        # actually create the band
        dances.append(Dance(
            date = date_from_string(dance_date), # TODO: make an actual datetime
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
        
