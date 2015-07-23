

class Dance():
    def __init__(self, date, location, band, caller):
        self.date = date
        self.location = location
        self.band = band
        self.caller = caller

    def display(self):
        print(self.date, self.band.name, self.caller.name)

class Band():
    def __init__(self, name, members):
        self.name = name
        self.members = members

class Person():
    def __init__(self, name, location="Bay Area"):
        self.name = name
        self.location = location

def parse_file(filename):
    dances = []
    lines = open(filename).readlines()

    for l in lines:
        (date, location, caller, band_info) = l.split(",", 3)

        print(band_info)
        (band_name, band_members) = band_info.split("(")
        band_members_list = band_members[:-1].split(",")
        # TODO: band and caller locations
        
        dances.append(Dance(
            date = date.strip(), # TODO: make an actual datetime
            location = location.strip(),
            band = Band(
                name = band_name.strip(),
                members = [Person(n.strip()) for n in band_members_list],
            ),
            caller = Person(caller.strip())
        ))
    
    return dances

if __name__ == "__main__":
    filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    dances = parse_file(filename)
    for d in dances:
        d.display()
        
