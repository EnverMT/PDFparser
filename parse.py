import os

from pdfminer.high_level import extract_text


def parsePDF(source_folder: str, result_folder: str):
    """
    Parses all PDF files in ./pdf/ directory to Text and creates similar folder structure is ./result_txt/ folder
    """
    path_base = os.getcwd()
    path_pdf = os.path.join(path_base, source_folder)
    path_result = os.path.join(path_base, result_folder)

    for root, d_names, f_names in os.walk(path_pdf):
        for f in f_names:
            filename = f.split('.')[0]
            path_diff = os.path.relpath(root, path_pdf)

            if not os.path.exists(os.path.join(path_result, path_diff)):
                os.makedirs(os.path.join(path_result, path_diff))

            file = open(f'{path_result}\\{path_diff}\\{filename}.txt', 'w', encoding='utf-8')
            file.write(extract_text(os.path.join(root, f)))
            file.close()
            print(f"File parsed: '{filename}'")