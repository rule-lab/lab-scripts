"""
This is a script for applying a custom color gradient to a selection in PyMOL
based on delta shift observed in NMR under differing conditions
"""

import cmd


def get_selection(fromfile=''):
    """
    After creating a csv file of residues paired to deltas (newlines between
    each residue), use this function to parse that into python
    """
    if not fromfile:
        print('No file specified...')
        return None
    residues = []
    with open(fromfile, 'r') as inp:
        for l in inp.readlines():
            if l.strip():
                r, d = l.split(',')
                residues.append((r.strip(), float(d.strip())))
    return residues

 
def apply_gradient(selection, start_color='blue', end_color='yellow'):
    """
    This function applies a gradient to the selection. It works with either
    a string color name which exists in the PyMOL color index, or custom RGB
    values.
    """
    deltas = []
    for r, d in selection:
        deltas.append(d)
    #Get the dynamic range of the deltas
    delta_min = min(deltas)
    delta_dynrange = max(deltas) - delta_min
    #Create a dictionary of colors from PyMOL
    color_dict = {}
    for col, num in cmd.get_color_indices():
        color_dict[col] = cmd.get_color_tuple(num)
    #Get the RGB values of the start color
    try:
        int(start_color[0])
    except ValueError:
        start_rgb = color_dict[start_color]
    else:
        start_rgb = start_color
    #Get the RGB values of the end color
    try:
        int(end_color[0])
    except ValueError:
        end_rgb = color_dict[end_color]
    else:
        end_rgb = end_color
    #Get the dynamic range for RGB values
    rgb_dynrange = []
    for i in range(3):
        rgb_dynrange.append(end_rgb[i]-start_rgb[i])
    print(rgb_dynrange)
    #Apply the coloring to each residue in the selection
    tick = 0
    for r, d in selection:
        cmd.select(name='gradient', selection='resi {0}'.format(r))
        change = (d - delta_min) / delta_dynrange
        res_red = start_rgb[0] + change * rgb_dynrange[0]
        res_gre = start_rgb[1] + change * rgb_dynrange[1]
        res_blu = start_rgb[2] + change * rgb_dynrange[2]
        cmd.set_color('grad{0}'.format(tick), [res_red, res_gre, res_blu])
        cmd.color('grad{0}'.format(tick), 'gradient')
        tick += 1
