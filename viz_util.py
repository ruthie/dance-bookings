from datetime import timedelta, date
import math

def class_name_for_date_with_prefix(prefix, date):
    return "{}-{}".format(prefix, str(date))

def get_location_html_for_dances(dances, css_prefix):
    # first we need to sort the dances by location
    dances_by_location = {}
    for d in dances:
        if d.location not in dances_by_location:
            dances_by_location[d.location] = []
        dances_by_location[d.location].append(d)

    start_html = '<table><tr>'
    end_html = '</tr></table>'
    html = start_html

    # let's sort locations alphabetically
    for location in sorted(dances_by_location.keys()):
        # skip locations with few dances
        # these are all special events, and not good comparisons for other locations
        if len(dances_by_location[location]) < 7:
            continue
            
        location_html = get_location_html(dances_by_location[location], css_prefix)
        html = html + '<td>'+ location_html + '</td>'

    html = html + end_html
    
    return html
    
def get_location_html(dances, prefix):
    # todo: sort dances by date
    start_html = '<h3>{}</h3><table><tr>'.format(dances[0].location)
    end_html = '</tr></table>'
    html = start_html

    row_length = math.ceil(len(dances)/7.0)
    for i in range(len(dances)):
        if i % row_length == 0:
            html = html  + '</tr><tr>'
        d = dances[i]
        # todo: actually correct thing for dates
        html = html + '<td><div class="day tooltip {}"></td>'.format(class_name_for_date_with_prefix(prefix, d.date))
        
    html = html + end_html
    
    return html

def get_calendar_html_for_date_range(start_date, end_date, css_prefix):
    start_html = '<table>'
    end_html = '</table>'
    row_start = "<tr>"
    row_end = "</tr>\n"

    # need to pad at the beginning and end to get a rectangular grid
    extra_days_start = start_date.weekday() + 1
    start_date_with_padding = start_date - timedelta(days=extra_days_start)

    extra_days_end = 5 - end_date.weekday()
    if extra_days_end == -1:
        extra_days_end = 6
    end_date_with_padding = end_date + timedelta(days=extra_days_end)
    
    html = start_html

    # first we need a row with years in it
    next_date = start_date_with_padding
    row = row_start
    while next_date < end_date_with_padding:
        # figure out how many columns until it's not this year
        # we actually want start of next year or the end of the graph, whichever comes first
        end_of_week = next_date + timedelta(days=7)
        start_of_next_year = min(date(year=end_of_week.year + 1, month=1, day=1), end_date_with_padding + timedelta(days=1))
        time_until_next_year = start_of_next_year - end_of_week
        # we round down so that the next label is on a column that starts
        weeks_until_next_year = max(int(time_until_next_year.days/7 +1), 1)

        row = row + "<td colspan={1}>{0} </td>".format(end_of_week.year, weeks_until_next_year)

        next_date = next_date + timedelta(days=7*weeks_until_next_year )

    html = html + row + row_end        
    
    # the first row of the table is sundays, second row mondays, etc.
    for i in range(7):
        next_date = start_date_with_padding + timedelta(days=i)

        html = html + row_start
        while next_date <= end_date_with_padding:
            html = html + '<td><div class="day tooltip {}"></td>'.format(class_name_for_date_with_prefix(css_prefix, next_date))
            next_date = next_date + timedelta(days=7) # a week later!
        
        html = html + row_end

    html = html + end_html
    return html

def get_css_string(dances, prefix, key_generator):
    css = ''
    for dance in dances:
        class_name = class_name_for_date_with_prefix(prefix, dance.date)
        dance_css = '''
.%s {
    background-color: #%s;
}

.%s:after {
    content: "%s";
}
''' % (class_name, key_generator(dance), class_name, str(dance))
        css = css + dance_css
        
    return css
