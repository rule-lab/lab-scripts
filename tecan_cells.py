#!/usr/bin/python

"""
Calculates the volume of yeast cell culture to add to plates for tecan
fluorescence measurements. Uses typical default values, but all of them may be
modified via argument or script modification.

Author: Paul Barton
"""

import argparse
import datetime
import os.path


#Defaults
cell_density = 23000000  # Cells per mL per OD
target_cells = 10000000  # Typical ranges are 10^6 to 10^7
dilution_factor = 20  # Measuring yeast cultures on spec; I recommend 20-fold
num_of_samples = False


def parser():
    p = argparse.ArgumentParser(description='Tecan Cells Parser')
    p.add_argument('-t', '--target', action='store', default=target_cells,
                  help='The desired number of cells in the sample.')
    p.add_argument('-D', '--density', action='store', default=cell_density,
                  help='The number of cells per mL per OD.')
    p.add_argument('-d', '--dilution', action='store', default=dilution_factor,
                  help='''The dilution factor used in measuring culture ODs;
                  should be a positive value, default is 20.''')
    p.add_argument('-s', '--samples', action='store', default=num_of_samples,
                  help='The amount of samples you would like to enter.')
    p.add_argument('-n', '--number', action='store_true', default = False,
                   help='''Number the samples in the order entered, instead of
                   naming them''')
    return p.parse_args()

def startReport(report, args):
    report.write('''Report generated on {0}\n
Cell Density: {1} (cells per mL per OD)
Target Cell Number: {2}
Dilution Factor: {3}\n'''.format(datetime.datetime.now().isoformat(),
                               args.density, args.target, args.dilution))

def prettyCenter(item, center_length, max_chars):
    item = str(item)
    if len(item) > max_chars:
        item = item[:max_chars]
    return item.center(center_length)

def main():
    args = parser()
    if not args.samples:
        while True:
            try:
                amount = int(raw_input('Amount of samples to be entered? '))
            except ValueError:
                print('Invalid value, must be an integer.')
            else:
                break
    else:
        amount = int(args.samples)
    with open('tc_report.txt', 'a') as report:
        startReport(report, args)
        report.write('Amount of Samples: {0}\n\n'.format(num_of_samples))
        samples = []
        for i in xrange(amount):
            if args.number:
                name = str(i + 1)
            else:
                name = raw_input('Sample name? ')
            od_req = 'OD-600 for {0} (diluted)? '.format(name)
            while True:
                try:
                    od = float(raw_input(od_req))
                except ValueError:
                    print('Invalid value, must be a number')
                else:
                    break
            
            samples.append((name, od))
        th = '|        Sample        |    OD-600    |    Cells/mL    |  Volume(uL) for {0} cells  |\n'
        report.write(th.format(args.target))
        for c in range(len(th.format(args.target)) - 1):
            report.write('-')
        report.write('\n')
        for n, o in samples:
            od = o * args.dilution
            cpml = od * args.density
            vol = str((args.target / cpml) * 1000)
            vcen = 25 + len(str(args.target))
            s_line = '|{0}|{1}|{2}|{3}|\n'.format(prettyCenter(n, 22, 22),
                                                 prettyCenter(od, 14, 6),
                                                 prettyCenter(cpml, 16, 12),
                                                 prettyCenter(vol, vcen, 4))
            report.write(s_line)
            print('Use {0} of {1} for {2} cells.'.format(vol, n, args.target))
        report.write('\n')
        print('A report of these results was saved to')
        print(os.path.abspath('tc_report.txt'))

if __name__ == '__main__':
    main()
