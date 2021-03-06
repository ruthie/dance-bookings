from datetime import date
from collections import OrderedDict, Counter

BOOKERS_FOR_LOCATIONS = {
    'Berkeley': 'Erik Hoffman',
    'Hayward': 'Kelsey Hartman',
    'SF': 'Chris Knepper',
    'Palo Alto': 'Alan Winston',
    'Queer Contra': 'Margaret Pigman',
    'Circle Left': 'Margaret Pigman',
    'San Jose': 'Shirley Worth',
    'San Rafael': 'Susan Amato',
    'Santa Rosa': 'Michael Martin',
    'Petaluma': 'Craig Meltzner',
    'Sebastapol': 'Andy Westbom'
}

class Dance():
    def __init__(self, date, location, band, callers):
        self.date = date
        self.location = location
        self.band = band
        self.callers = callers

    def __str__(self):
        callers_str = ", ".join([str(c) for c in self.callers])        
        return "{self.date}, {self.location}, {self.band}, {callers_str}".format(**locals())

class Band():
    def __init__(self, name, members):
        self.members = members
        if name == "":
            names = [m.name for m in members]
            names.sort()
            name = ", ".join(names)
        self.name = name

    def __str__(self):
        s = self.name + " (" + ", ".join([str(m) for m in self.members]) + ")"
        return s

class Person():
    def __init__(self, name, location):
        self.name = name
        if location is None:
            location = "Bay Area"
        self.location = location

    def __str__(self):
        return self.name + "/" + self.location

class Location():
    def __init__(self, name, booker):
        self.name = name
        self.booker = booker

def get_booker_for_location(l):
    if l in BOOKERS_FOR_LOCATIONS:
        return BOOKERS_FOR_LOCATIONS[l]

    return "Unknown"
        
def get_name_location(s):
    if "[" not in s:
        return s.strip(), None

    (name, loc) = s.split("[")
    return name.strip(), loc.strip()[:-1].strip()

def get_gigs_for_band(band_name, dances):
    gigs = [d for d in dances if d.band.name == band_name]
    return gigs

def get_bands_for_musician(musician_name, dances):
    bands = [d.band.name for d in dances if musician_name in [m.name for m in d.band.members]]
    return bands

def date_from_string(s):
    (month, day, year) = s.strip().split("/")
    return date(month=int(month), day=int(day), year=int(year))

def parse_file(filename):
    dances = []
    lines = open(filename).readlines()

    for l in lines:
        (dance_date, dance_location, callers, band_info) = l.split(",", 3)
        band_info = band_info[1:-2] # get rid of newline and quotes

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

        dance_location = dance_location.strip()
            
        # actually create the band
        dances.append(Dance(
            date = date_from_string(dance_date),
            location = Location(
                name = dance_location,
                booker = get_booker_for_location(dance_location)
            ),
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

def get_most_booked_bands(dances):
    return frequency_dict(dances, lambda x: [x.band])

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

def get_all_dances():
    dance_filenames = [
        '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv',
        '/Users/ruthie/Desktop/contra_bookings/queer_contra_bookings.csv',
        '/Users/ruthie/Desktop/contra_bookings/hayward_bookings.csv',
        '/Users/ruthie/Desktop/contra_bookings/nbcds_bookings.csv',
    ]

    dances = []
    for input_filename in dance_filenames:
        dances = dances + parse_file(input_filename)
    return dances

def is_band_local(band):
    locations = [m.location for m in band.members]
    return 'Bay Area' in locations

def get_top_local_bands(dances):
    local_band_gigs = [d.band.name for d in dances if is_band_local(d.band)]
    most_booked_bands = Counter(local_band_gigs)
    bands = most_booked_bands.most_common()
    return bands

def print_local_band_info(dances):
    bands = get_top_local_bands(dances)[:11]
    for (name, count) in bands:
        print("* {} ({})".format(name, count))

    for (band_name, _) in bands[:11]:
        gigs = get_gigs_for_band(band_name, dances)
        gig_counts = Counter(frequency_dict(gigs, lambda x: [x.location]))

        print(band_name, len(gig_counts))

def print_bands_for_each_musician(dances):
    musicians = get_most_booked_musicians(dances)
    counter = Counter(musicians)
    for (m, count) in counter.most_common(20):
        bands = get_bands_for_musician(m, dances)
        counter = Counter(bands)
        num_bands = len(counter.most_common())
        most_booked_band = counter.most_common(1)[0][1]
        import math
        percentage_with_most_booked_band = math.trunc(100.0*most_booked_band/len(bands))
        
        print("* {} ({}) bands: {}, {}".format(m, count, num_bands, percentage_with_most_booked_band))
        print(counter.most_common())
    
if __name__ == "__main__":
    dances = get_all_dances()
