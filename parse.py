import datetime
import os
import re

from pdfminer.high_level import extract_text


class Parse:
    def __init__(self, source_folder: str, result_folder: str):
        self.path_base = os.getcwd()
        self.path_pdf = os.path.join(self.path_base, source_folder)
        self.path_result = os.path.join(self.path_base, result_folder)
        self._count_files()
        self.progress_reported_time = datetime.datetime.utcnow()

    def _count_files(self):
        self.file_count = 0
        for root_dir, cur_dir, files in os.walk(self.path_pdf):
            self.file_count += len(files)

        self.result_file_count = 0
        for root_dir, cur_dir, files in os.walk(self.path_result):
            self.result_file_count += len(files)

    def parse_pdf(self, skip_parsed_files: bool = False):
        """
        Parses all PDF files in Source folder to Text and creates similar folder structure is Result folder
        """
        count = 0

        for root, d_names, f_names in os.walk(self.path_pdf):
            for f in f_names:
                if not f.endswith('.pdf'):
                    print(f'Not PDF file. Skipped. Filename={f}')
                    continue

                count += 1
                filename = f.split('.')[0]
                path_diff = os.path.relpath(root, self.path_pdf)

                # Create folder if not exist
                if not os.path.exists(os.path.join(self.path_result, path_diff)):
                    os.makedirs(os.path.join(self.path_result, path_diff))

                file_path = f'{self.path_result}\\{path_diff}\\{filename}.txt'

                if os.path.exists(file_path) and skip_parsed_files:
                    self._print_progress(count / self.result_file_count,
                                         message=f'''Files count: {count}/{self.file_count} 
                                         | File already exists, Skipping: {f}''')
                    continue

                file = open(file_path, 'w', encoding='utf-8')
                file.write(extract_text(os.path.join(root, f)))
                file.close()
                self._print_progress(count / self.result_file_count,
                                     message=f'Files count: {count}/{self.file_count} | PDF file parsed: {f}')
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
                res_dict['Apparatus'] = self._get_text_part(os.path.join(root, f), ['[\d+][\.] Apparatus'],
                                                            ['[\d+][\.] Reagents',
                                                             '[\d+][\.] Procedure',
                                                             '[\d+][\.] Calibration'])
                res_dict['Reagents'] = self._get_text_part(os.path.join(root, f), ['[\d+][\.] Reagents'],
                                                           ['[\d+][\.] Procedure',
                                                            '[\d+][\.] Calibration'])
                res_dict['Standart_ID'] = self._get_text_exact(os.path.join(root, f), 'Designation: (.+)')
                res_dict['Method_name'] = self._get_text_part(os.path.join(root, f), ['Standard Test Methods'],
                                                              ['This standard is issued under'])

                result.append(res_dict)

                count += 1
                self._print_progress(count / self.result_file_count,
                                     message=f'Files count: {count}/{self.result_file_count} | TXT file parsed: {f}')
        return result

    @staticmethod
    def _get_text_part(file_path: str, start_text: list[str], end_text: list[str]) -> str:
        """
        Get text between Start_text and End_text
        """
        content = str()
        with open(file_path, 'r', encoding='utf-8') as file:
            body = False
            for line in file:
                if re.search('|'.join(start_text), line) and not body:
                    body = True
                    continue
                if re.search('|'.join(end_text), line) and body:
                    break
                if body:
                    content += line
        return content.strip()

    @staticmethod
    def _get_text_exact(file_path: str, re_pattern: str) -> str:
        """
        Get one line of text matching the pattern RePattern
        """
        content = str()
        with open(file_path, 'r', encoding='utf-8') as file:
            body = False
            for line in file:
                if re.search(re_pattern, line) and not body:
                    return re.search(re_pattern, line).group(1)
        return content.strip()

    def _print_progress(self, progress_value: float, message: str):
        if (datetime.datetime.utcnow() - self.progress_reported_time).total_seconds() < 1:
            return

        self.progress_reported_time = datetime.datetime.utcnow()
        print(f'Progress: {progress_value * 100 :.2f}% | {message}')