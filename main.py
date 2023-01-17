import pandas as pd

from parse import parse

p = parse(source_folder='pdf', result_folder='result_txt')
#p.parsePDF() # Use parse only once, After parsing should be commented
res = p.parse_result_files()

df = pd.DataFrame(data=res)

print(df)

df.to_excel('db.xlsx', index=False)