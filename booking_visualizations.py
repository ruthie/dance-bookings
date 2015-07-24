from datetime import date
from bookings import parse_file
from viz_util import *

def write_html(dances, filename):
    f = open(filename, 'w')

    dance_dates = [d.date for d in dances]
    (start_date, end_date) = (min(dance_dates), max(dance_dates))
    
    band_html = get_calendar_html_for_date_range(start_date, end_date, "band")
    caller_html = get_calendar_html_for_date_range(start_date, end_date, "caller")
    
    html = '''<head>
  <title>Bay Area Dance Booking Visualization</title>
  <link rel="stylesheet" type="text/css" href="viz.css">
</head>
<body>
  <h1>Bay Area Contra Dance Bookings</h1>
  <h2>bands</h2>
  {}
  <h2>callers</h2>
  {}
</body>'''.format(band_html, caller_html)
    f.write(html)

def write_css(dances, css_filename):
    f = open(css_filename, 'w')

    width_percentage = 1.0 / (len(dances) / 7 + 1)
    
    start_css = '''
body {
    font-family: sans-serif;
    font-size: xx-large;
}

.day {
    width: 10px;
    height: 10px;
}

table {
    border-spacing: 1px;
}
'''

    band_color_map = make_color_map([d.band.name for d in dances])
    caller_color_map = make_color_map([d.callers[0].name for d in dances])
    
    band_css = get_css_string(dances, "band", lambda d: band_color_map[d.band.name])
    caller_css = get_css_string(dances, "caller", lambda d: caller_color_map[d.callers[0].name])

    f.write(start_css)
    f.write(band_css)
    f.write(caller_css)

def write_dance_visualizations():
    input_filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    html_filename = '/Users/ruthie/Desktop/contra_bookings/viz.html'
    css_filename = '/Users/ruthie/Desktop/contra_bookings/viz.css'

    dances = parse_file(input_filename)

    write_html(dances, html_filename)
    write_css(dances, css_filename)
    
if __name__ == "__main__":
    write_dance_visualizations()
