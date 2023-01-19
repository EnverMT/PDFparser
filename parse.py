import os
import re

from pdfminer.high_level import extract_text


class parse():
    def __init__(self, source_folder: str, result_folder: str):
        self.path_base = os.getcwd()
        self.path_pdf = os.path.join(self.path_base, source_folder)
        self.path_result = os.path.join(self.path_base, result_folder)
        self._count_files()

    def _count_files(self):
        self.file_count = 0
        for root_dir, cur_dir, files in os.walk(self.path_pdf):
            self.file_count += len(files)

        self.result_file_count = 0
        for root_dir, cur_dir, files in os.walk(self.path_result):
            self.result_file_count += len(files)

    def parsePDF(self, skip_parsed_files: bool = False):
        """
        Parses all PDF files in Source folder to Text and creates similar folder structure is Result folder
        """
        parsed_files = 0

        for root, d_names, f_names in os.walk(self.path_pdf):
            for f in f_names:
                if not f.endswith('.pdf'):
                    print(f'Not PDF file. Skipped. Filename={f}')
                    continue

                parsed_files += 1
                completion_percent = parsed_files / self.file_count
                filename = f.split('.')[0]
                path_diff = os.path.relpath(root, self.path_pdf)

                # Create folder if not exist
                if not os.path.exists(os.path.join(self.path_result, path_diff)):
                    os.makedirs(os.path.join(self.path_result, path_diff))

                file_path = f'{self.path_result}\\{path_diff}\\{filename}.txt'

                if os.path.exists(file_path) and skip_parsed_files == True:
                    print(
                        f'Progress: {completion_percent * 100:.2f}% File {parsed_files}/{self.file_count} File already exists, Skipping: {filename}')
                    continue

                file = open(file_path, 'w', encoding='utf-8')
                file.write(extract_text(os.path.join(root, f)))
                file.close()
                print(
                    f"Progress: {completion_percent * 100:.2f}% File {parsed_files}/{self.file_count} parsed: '{filename}'")
        self._count_files()

    def parse_result_files(self) -> list:
        """
        Parse all TXT files to Pandas Dataframe
        """
        result = []
        count = 0
        for root, d_names, f_names in os.walk(self.path_result):
            for f in f_names:
                res_dict = dict()
                res_dict['file_name'] = f
                res_dict['Apparatus'] = self._get_text_part(os.path.join(root, f), '[\d+][\.] Apparatus',
                                                            ['[\d+][\.] Reagents',
                                                             '[\d+][\.] Procedure',
                                                             '[\d+][\.] Calibration'])
                res_dict['Reagents'] = self._get_text_part(os.path.join(root, f), '[\d+][\.] Reagents',
                                                           ['[\d+][\.] Procedure',
                                                            '[\d+][\.] Calibration'])
                res_dict['Standart_ID'] = self._get_text_exact(os.path.join(root, f), 'Designation: (.+)')
                res_dict['Method_name'] = self._get_text_part(os.path.join(root, f), 'Standard Test Methods',
                                                              ['This standard is issued under'])

                result.append(res_dict)

                count += 1
                print(f'Progress: {count / self.result_file_count * 100 :.2f}% TXT file parsed: {f}')
        return result

    def _get_text_part(self, filePath: str, start_text: str, end_text: str) -> str:
        """
        Get text between Start_text and End_text
        """
        content = str()
        with open(filePath, 'r', encoding='utf-8') as file:
            body = False
            for line in file:
                if re.search(start_text, line) and body == False:
                    body = True
                    continue
                if re.search('|'.join(end_text), line) and body == True:
                    break
                if body:
                    content += line
        return content.strip()

    def _get_text_exact(self, filePath: str, rePattern: str) -> str:
        """
        Get one line of text matching the pattern RePattern
        """
        content = str()
        with open(filePath, 'r', encoding='utf-8') as file:
            body = False
            for line in file:
                if re.search(rePattern, line) and body == False:
                    return re.search(rePattern, line).group(1)
        return content.strip()