import math

# coloring related things
def int_to_six_digit_hex(i):
    return int_to_n_digit_hex(i, 6)

def int_to_two_digit_hex(i):
    return int_to_n_digit_hex(i, 2)

def int_to_n_digit_hex(i, digits):
    h = hex(int(i))
    # cut off the initial "0x"
    h = h[2:]
    while len(h) < digits:
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
