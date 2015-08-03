import sexmachine.detector as gender
import spectra
from color_util import int_to_two_digit_hex

d = gender.Detector(case_sensitive=False)

def gender_color_for_people(people):
    gender_values = [get_gender_for_name(p.name) for p in people]
    average_gender = sum(gender_values)/len(gender_values)

    # now we turn the number into a color.  Yellow for men, red for women.
    scale = spectra.scale(['red', 'purple'])
    # this library returns the hexcode with the hash, we don't expect it, so chop it off
    color = scale(average_gender).hexcode[1:]
    return color
    
def get_gender_for_name(name):
    # let's hard code some commonly booked people here
    if name == 'Chris Knepper':
        return 1.0
    elif name == 'Yoyo Zhou':
        return 1.0
    elif name == 'Topher Gayle':
        return 1.0
    elif name == 'Charlie Fenton':
        return 1.0
    elif name == 'Kalia Kliban':
        return 0.0
    elif name == 'Robin Steen':
        return 0.0
    elif name == 'Frannie Mar':
        return 0.0
    
    first_name = name.split(" ")[0]
    gender_word = d.get_gender(first_name)

    word_to_value = {
        'male': 1.0,
        'mostly_male': 0.8,
        'andy': 0.5,
        'mostly_female': 0.2,
        'female': 0.0,
    }

    return word_to_value[gender_word]
