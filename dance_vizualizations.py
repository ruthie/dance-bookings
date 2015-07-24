from datetime import date
from bookings import parse_file
from viz import write_html, write_css

def write_dance_visualizations():
    input_filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    html_filename = '/Users/ruthie/Desktop/contra_bookings/viz.html'
    css_filename = '/Users/ruthie/Desktop/contra_bookings/viz.css'
    
    dances = parse_file(input_filename)
    dance_dates = [d.date for d in dances]

    write_html(min(dance_dates), max(dance_dates), html_filename, "caller")
    write_css(dances, css_filename, "caller", lambda x: x.callers[0].name)

    #write_html(min(dance_dates), max(dance_dates), html_filename, "band")
    #write_css(dances, css_filename, "band", lambda x: x.band.name)
    
if __name__ == "__main__":
    write_dance_visualizations()
