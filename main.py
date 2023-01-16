import os
from pdfminer.high_level import extract_text


path_current = os.getcwd()
path_pdf = os.path.join(path_current, "pdf")

for root, d_names, f_names in os.walk(path_pdf):
    for f in f_names:
        text = extract_text(os.path.join(root, f))
        filename = f.split('.')[0]
        file = open(f'result_txt\\{filename}.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()