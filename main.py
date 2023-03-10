import sqlite3

import pandas as pd

from parse import Parse

p = Parse(source_folder='pdf', result_folder='result_txt')
# p.parsePDF(skip_parsed_files=True)  # Use parse only once, After parsing should be commented
res = p.parse_result_files()

df = pd.DataFrame(data=res)

# print(df)

# Something wrong with Excel file, some error with not allowed symbol in .xlsx file
# df.to_excel('db.xlsx', index=False)

# Export parse result to Sqlite3 database
conn = sqlite3.connect('db.sqlite')
table_name = 'ASTM'

query = f'DROP TABLE IF EXISTS {table_name}'
conn.execute(query)
conn.commit()
print("Table Dropped")

query = f'''Create table if not Exists {table_name} (file_name text, 
                                                    Apparatus text, 
                                                    Reagents text, 
                                                    Standart_ID text, 
                                                    Method_name text)'''
conn.execute(query)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.commit()
print("Table saved to Database")

conn.close()