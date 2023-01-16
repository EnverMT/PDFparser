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

    def getTextPart(self, start_text: str, end_text: list[str]) -> str:
        res_dict = dict()
        for root, d_names, f_names in os.walk(self.path_result):
            for f in f_names:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                    content = str()
                    body = False
                    for line in file:
                        if re.search(start_text, line) and body == False:
                            body = True
                            continue
                        if re.search('|'.join(end_text), line) and body == True:
                            body = False
                            continue
                        if body:
                            content += line
                    res_dict[f] = content
        return res_dict