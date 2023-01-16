from parse import parse

p = parse(source_folder='pdf', result_folder='result_txt')
p.parsePDF()
print(p.getTextPart('Apparatus', ['Reagents','Calibration']))

# to do:
# parse TXT to Excel file by chapters