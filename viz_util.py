from datetime import timedelta, date
import math

def class_name_for_date_with_prefix(prefix, date):
    return "{}-{}".format(prefix, str(date))

def get_calendar_html_for_date_range(start_date, end_date, css_prefix):
    start_html = '<table>'
    end_html = '</table>'

    # need to pad at the beginning and end to get a rectangular grid
    extra_days_start = start_date.weekday() + 1
    start_date_with_padding = start_date - timedelta(days=extra_days_start)

    extra_days_end = 5 - end_date.weekday()
    if extra_days_end == -1:
        extra_days_end = 6
    end_date_with_padding = end_date + timedelta(days=extra_days_end)
    
    html = start_html

    # the first row of the table is sundays, second row mondays, etc.
    for i in range(7):
        next_date = start_date_with_padding + timedelta(days=i)
        row_start = "<tr>"
        row_end = "</tr>\n"

        html = html + row_start
        while next_date <= end_date_with_padding:
            html = html + '<td><div class="day {}"></td>'.format(class_name_for_date_with_prefix(css_prefix, next_date))
            next_date = next_date + timedelta(days=7) # a week later!
        
        html = html + row_end

    html = html + end_html
    return html

def get_css_string(dances, prefix, key_generator):
    css = ''
    for dance in dances:
        dance_css = '''
.%s {
    background-color: #%s;
}
''' % (class_name_for_date_with_prefix(prefix, dance.date), key_generator(dance))
        css = css + dance_css
        
    return css


# coloring related things
def int_to_six_digit_hex(i):
    h = hex(int(i))
    # cut off the initial "0x"
    h = h[2:]
    while len(h) < 6:
        h = "0" + h
    return h

# assigns colors evenly over the full range of possible colors
def make_color_map(keys):
    keys_list = list(set(keys))
    keys_list.sort()
    m = {}

    max_color = math.pow(16, 6)
    for i in range(len(keys_list)):
        k = keys_list[i]
        int_val = math.floor(max_color * (i * 1.0/len(keys_list)))
        m[k] = int_to_six_digit_hex(int_val)

    return m
