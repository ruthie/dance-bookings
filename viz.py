from datetime import timedelta, date

# TODO: add support for multiple dances per day
# TODO: add support for bands
# TODO: tooltips

def class_name_for_date(d):
    return "day-{}".format(str(d))

def write_html(start_date, end_date, filename):
    f = open(filename, 'w')
    
    start_html = '''<head>
  <link rel="stylesheet" type="text/css" href="viz.css">
</head>
<body>
  <table>'''
    end_html = '''  </table>
</body>'''
    f.write(start_html)
    
    # TODO: shift so that Sunday is on far Left
    # need to pad at the beginning and end to get a rectangular grid
    extra_days_start = start_date.weekday()
    start_date_with_padding = start_date - timedelta(days=extra_days_start)

    extra_days_end = 6 - end_date.weekday()
    end_date_with_padding = end_date + timedelta(days=extra_days_end)
    
    next_date = start_date_with_padding
    while next_date <= end_date_with_padding:
        row_start = "<tr>"
        row_end = "</tr>\n"
        f.write(row_start)

        for i in range(7):
            next_date = next_date + timedelta(days=1)
            f.write('<td><div class="day {}"></td>'.format(class_name_for_date(next_date)))
        
        f.write(row_end)

    f.write(end_html)

def write_css(dances, filename):
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
''' % (class_name_for_date(dance.date), color_for_string(dance.band.name))
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

    
