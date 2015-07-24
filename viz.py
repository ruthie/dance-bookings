from datetime import timedelta, date

# TODO: add support for callers
# TODO: add support for multiple dances per day
# TODO: tooltips

def class_name_for_date_with_prefix(prefix, date):
    return "{}-{}".format(prefix, str(date))

def get_calendar_html_for_date_range(start_date, end_date, css_prefix):
    start_html = '<table>'
    end_html = '</table>'

    html = start_html
    next_date = start_date
    while next_date <= end_date:
        row_start = "<tr>"
        row_end = "</tr>\n"

        html = html + row_start
        for i in range(7):
            html = html + '<td><div class="day {}"></td>'.format(class_name_for_date_with_prefix(css_prefix, next_date))
            next_date = next_date + timedelta(days=1)
        
        html = html + row_end

    html = html + end_html
    return html

    
def write_html(start_date, end_date, filename, prefix):
    f = open(filename, 'w')
    
    start_html = '''<head>
  <link rel="stylesheet" type="text/css" href="viz.css">
</head>
<body>'''
    end_html = '''
</body>'''
    f.write(start_html)
    
    # need to pad at the beginning and end to get a rectangular grid
    extra_days_start = start_date.weekday() + 1
    start_date_with_padding = start_date - timedelta(days=extra_days_start)

    extra_days_end = 5 - end_date.weekday()
    if extra_days_end == -1:
        extra_days_end = 6
    end_date_with_padding = end_date + timedelta(days=extra_days_end)
    
    f.write(get_calendar_html_for_date_range(start_date_with_padding, end_date_with_padding, prefix))
    f.write(end_html)

def write_css(dances, filename, prefix, key_generator):
    f = open(filename, 'w')

    start_css = '''
.day {
    width: 20px;
    height: 20px;
}
'''
    for dance in dances:
        dance_css = '''
.%s {
    background-color: #%s;
}
''' % (class_name_for_date_with_prefix(prefix, dance.date), color_for_string(key_generator(dance)))
        f.write(dance_css)
        
    f.write(start_css)

def color_for_string(s):
    # TODO: handle spaces
    # TODO: this should somehow deal with common prefixes
    s = s.lower()

    if s.startswith("the "):
        s = s[4:]
    
    return hex_chars_for_char(s[0]) + hex_chars_for_char(s[1]) + hex_chars_for_char(s[2])

def hex_chars_for_char(c):
    scale_factor = 16*16/26
    int_val = (ord(c) - ord('a')) * scale_factor
    # remove the "0x"
    hex_val = hex(int_val)[2:]
    return hex_val

    