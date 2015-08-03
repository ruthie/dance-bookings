from datetime import date
from random import choice
from string import lowercase

from bookings import parse_file
from viz_util import *
from gender import gender_color_for_people
from color_util import make_color_map


def write_dance_visualizations():
    dance_filenames = [
        '/Users/ruthie/Desktop/contra_bookings/bacds_bookings.csv',
        '/Users/ruthie/Desktop/contra_bookings/queer_contra_bookings.csv'
    ]
    html_filename = '/Users/ruthie/Desktop/contra_bookings/viz.html'
    css_filename = '/Users/ruthie/Desktop/contra_bookings/viz.css'

    dances = []
    for input_filename in dance_filenames:
        dances = dances + parse_file(input_filename)

    write_files(dances, 'viz')

def write_files(dances, filename):
    html_f = open(filename + '.html', 'w')
    css_f = open(filename + '.css', 'w')

    write_html_start(html_f)
    write_css_start(css_f)

    # setup: we need color maps for bands and callers
    band_color_map = make_color_map([d.band.name for d in dances])
    caller_color_map = make_color_map([d.callers[0].name for d in dances])
    location_color_map = make_color_map(
        [d.band.members[0].location for d in dances] + [d.callers[0].location for d in dances]
    )

    viz_specs = [
        (
            ' By Name',
            lambda d: band_color_map[d.band.name],
            lambda d: caller_color_map[d.callers[0].name],
        ),
        (
            ' By Home State',
            lambda d: location_color_map[d.band.members[0].location],
            lambda d: location_color_map[d.callers[0].location],
        ),
        (
            ' By Gender',
            lambda d: gender_color_for_people(d.band.members),
            lambda d: gender_color_for_people(d.callers),
        ),
    ]

    for viz in viz_specs:
        html, css = get_html_css_for_visualization(dances, *viz)
        html_f.write(html)
        css_f.write(css)

    write_html_end(html_f)

def get_html_css_for_visualization(dances, desc, band_color_generator, caller_color_generator):
    prefix = desc.lower().replace(' ', '-') + '-'
    band_prefix = 'band-' + prefix
    caller_prefix = 'caller-' + prefix
    
    band_html = get_location_html_for_dances(dances, band_prefix)
    caller_html = get_location_html_for_dances(dances, caller_prefix)

    html = '''<table class="viz-container"><tr>
<td>
<h2>Bands {0}</h2>
{1}
</td>
<td>
<h2>Callers {0}</h2>
{2}
</td></tr></table>'''.format(desc, band_html, caller_html)

    band_css = get_css_string(dances, band_prefix, band_color_generator)
    caller_css = get_css_string(dances, caller_prefix, caller_color_generator)
    css = band_css + caller_css
    
    return html, css
    
def write_html_start(f):
    start_html = '''<head>
  <title>Bay Area Contra Dance Booking Visualization</title>
  <link rel="stylesheet" type="text/css" href="viz.css">
</head>
<body>
<h1>Bay Area Contra Dance Bookings</h1>
'''
    f.write(start_html)

def write_html_end(f):
    f.write('</body>')

def write_css_start(f):
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

table.viz-container {
    width: 100%;
    padding-bottom: 50px;
}
'''
    f.write(start_css)
        
if __name__ == "__main__":
    write_dance_visualizations()
