from pathlib import Path
import pandas as pd
import sys
import pyarrow as pa
import pyarrow.parquet as pq
import json
from json_repair import repair_json

# data_dir = Path("src/data/annotated_m_split_courses")
# data = []
# for year in range(2000, 2023):    
#     for fname in data_dir.glob(f"0155zta11_ug_{year}_{year+1}*"):
        
#         ror, cat_type, year_1, year_2, page_number, col_number = fname.stem.split("_")[:6]
        
#         try:
#             with open(fname) as f:
#                 out = json.loads(repair_json(f.read()))
#                 for e in out:
#                     tmp = [e['Department'], e['Number'], e['Title'], e['Description'], page_number, col_number, year]
#                     data.append(tmp)
#         except:
#             print(f"Error reading {fname}")


# df = pd.DataFrame(data, columns=['Department', 'Number', 'Title', 'Description', 'page_number', 'col_number','year'])
# df.to_csv("src/data/annotated_data.csv", index=False)

df = pd.read_csv("src/data/annotated_data.csv")
df = df[~df.Number.isna() & ~df.Title.isna()]

# Check if there are any numbers that contain a digit
df = df[df.Number.str.contains(r"\d")]

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)