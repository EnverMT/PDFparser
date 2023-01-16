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
        Parses all PDF files in Source folder to Text and creates similar folder structure is Result folder
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

    def parse_result_files(self) -> str:
        """
        Parse all TXT files to Pandas Dataframe
        """
        result = []
        for root, d_names, f_names in os.walk(self.path_result):
            for f in f_names:
                res_dict = dict()
                res_dict['file_name'] = f
                res_dict['Apparatus'] = self.get_text_part(os.path.join(root,f), 'Apparatus', ['Reagents'])
                result.append(res_dict)
        return result

    def get_text_part(self, filePath, start_text, end_text):
        """
        Get text between Start_text and End_text
        """
        with open(filePath, 'r', encoding='utf-8') as file:
            content = str()
            body = False
            for line in file:
                if re.search(start_text, line) and body == False:
                    body = True
                    continue
                if re.search('|'.join(end_text), line) and body == True:
                    break
                if body:
                    content += line
            return content