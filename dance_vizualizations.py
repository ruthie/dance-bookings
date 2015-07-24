from datetime import date
from bookings import parse_file
from viz import *

def write_html(dances, filename):
    f = open(filename, 'w')

    dance_dates = [d.date for d in dances]
    (start_date, end_date) = (min(dance_dates), max(dance_dates))
    
    band_html = get_calendar_html_for_date_range(start_date, end_date, "band")
    caller_html = get_calendar_html_for_date_range(start_date, end_date, "caller")
    
    html = '''<head>
  <link rel="stylesheet" type="text/css" href="viz.css">
</head>
<body>
  <table>
    <tr>
      <td>{}</td>
      <td>{}</td>
    </tr>
  </table>
</body>'''.format(band_html, caller_html)
    f.write(html)

def write_css(dances, css_filename):
    f = open(css_filename, 'w')
    start_css = '''
.day {
    width: 20px;
    height: 20px;
}
'''    
    band_css = get_css_string(dances, "band", lambda x: x.band.name)
    caller_css = get_css_string(dances, "caller", lambda x: x.callers[0].name)

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
