import os
import re

from pdfminer.high_level import extract_text


class parse():
    def __init__(self, source_folder: str, result_folder: str):
        self.path_base = os.getcwd()
        self.path_pdf = os.path.join(self.path_base, source_folder)
        self.path_result = os.path.join(self.path_base, result_folder)

    def parsePDF(self):
        """
        Parses all PDF files in ./pdf/ directory to Text and creates similar folder structure is ./result_txt/ folder
        """

        for root, d_names, f_names in os.walk(self.path_pdf):
            for f in f_names:
                filename = f.split('.')[0]
                path_diff = os.path.relpath(root, self.path_pdf)

                if not os.path.exists(os.path.join(self.path_result, path_diff)):
                    os.makedirs(os.path.join(self.path_result, path_diff))

                file = open(f'{self.path_result}\\{path_diff}\\{filename}.txt', 'w', encoding='utf-8')
                file.write(extract_text(os.path.join(root, f)))
                file.close()
                print(f"File parsed: '{filename}'")

    def getTextPart(self, start_text : str, end_text : list[str]) -> str:
        result = str()
        body = False
        start = start_text
        if len(end_text) == 1:
            end = end_text[0]
        else:
            end = '|'.join(end_text)

        for root, d_names, f_names in os.walk(self.path_result):
            for f in f_names:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                    for line in file:
                        if re.search(start, line):
                            body = True
                            continue
                        if re.search(end, line) and body == True:
                            body = False
                            break
                        if body:
                            result += line
                    return result