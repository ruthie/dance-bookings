from datetime import date
from bookings import parse_file
from viz_util import *
from gender import gender_color_for_people
from color_util import make_color_map

def write_html(dances, filename):
    f = open(filename, 'w')

    dance_dates = [d.date for d in dances]
    (start_date, end_date) = (min(dance_dates), max(dance_dates))
    
    band_html = get_location_html_for_dances(dances, "band")
    caller_html = get_location_html_for_dances(dances, "caller")

    band_location_html = get_location_html_for_dances(dances, "band-loc")
    caller_location_html = get_location_html_for_dances(dances, "caller-loc")

    band_gender_html = get_location_html_for_dances(dances, "band-gender")
    caller_gender_html = get_location_html_for_dances(dances, "caller-gender")
    
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
  <h2>band homes</h2>
  {}
  <h2>caller homes</h2>
  {}
  <h2>band gender</h2>
  {}
  <h2>caller gender</h2>
  {}

</body>'''.format(band_html, caller_html, band_location_html, caller_location_html, band_gender_html, caller_gender_html)
    f.write(html)

def write_css(dances, css_filename):
    f = open(css_filename, 'w')

    width_percentage = 1.0 / (len(dances) / 7 + 1)
    
    start_css = '''
body {
    font-family: sans-serif;
    font-size: xx-large;
}

.tooltip:hover:after {
    display: inline;
    position: absolute;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 1px 1px 4px #000;
    background-color: #fff;
    margin-left: 5px;
    margin-top: -25px;
    padding: 3px;
}

.tooltip:after {
    display: none;
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
    location_color_map = make_color_map(
        [d.band.members[0].location for d in dances] + [d.callers[0].location for d in dances]
    )


    band_css = get_css_string(dances, "band", lambda d: band_color_map[d.band.name])
    caller_css = get_css_string(dances, "caller", lambda d: caller_color_map[d.callers[0].name])    
    band_location_css = get_css_string(dances, "band-loc", lambda d: location_color_map[d.band.members[0].location])
    caller_location_css = get_css_string(dances, "caller-loc", lambda d: location_color_map[d.callers[0].location])
    band_gender_css = get_css_string(dances, "band-gender", lambda d: gender_color_for_people(d.band.members))
    caller_gender_css = get_css_string(dances, "caller-gender", lambda d: gender_color_for_people(d.callers))

    f.write(start_css)
    f.write(band_css)
    f.write(caller_css)
    f.write(band_location_css)
    f.write(caller_location_css)
    f.write(band_gender_css)
    f.write(caller_gender_css)

    
    
def write_dance_visualizations():
    input_filename = '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv'
    html_filename = '/Users/ruthie/Desktop/contra_bookings/viz.html'
    css_filename = '/Users/ruthie/Desktop/contra_bookings/viz.css'

    dances = parse_file(input_filename)

    write_html(dances, html_filename)
    write_css(dances, css_filename)
    
if __name__ == "__main__":
    write_dance_visualizations()
