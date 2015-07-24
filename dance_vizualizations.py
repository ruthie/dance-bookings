from datetime import date
from bookings import parse_file
from viz import write_html, write_css

def write_dance_visualizations():
    # TODO: take start and end dates from list of dances
    start = date(year=2013, month=10, day=1)
    end = date(year=2015, month=9, day=30)
    write_html(start, end, '/Users/ruthie/Desktop/contra_bookings/viz.html')

    filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    dances = parse_file(filename)
    
    write_css(dances, '/Users/ruthie/Desktop/contra_bookings/viz.css')
    
if __name__ == "__main__":
    write_dance_visualizations()
