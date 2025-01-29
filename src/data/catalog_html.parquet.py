import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sys

# ----

# with open("src/data/html-catalog/urls-2014-2015.txt") as f:
#     course_urls = f.read().splitlines()


# ----

# course_data = []

# for url in course_urls:
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     courseblocks = soup.find_all('div', class_='courseblock')

#     for block in courseblocks:
#         title = block.find('p', class_='courseblocktitle').get_text(strip=True)
#         title = title.replace('\xa0', ' ')
#         description = block.find('p', class_='courseblockdesc').get_text(strip=True)

#         course_data.append({
#             'url': url,
#             'cat_type': url.split('/')[-4], 
#             'college': url.split('/')[-3],
#             'dept': url.split('/')[-2],
#             'title': title,
#             'description': description
#         })

#     sleep(1)

# df = pd.DataFrame(course_data)
# df.to_csv("src/data/html-catalog/2022-23-html-catalog.csv", index=False)

dfs = []
for yr in range(2014, 2023):
    d=pd.read_csv(f"src/data/html-catalog/{yr}-{str(yr+1)[-2:]}-html-catalog.csv")
    d['year'] = yr
    dfs.append(d)

df = pd.concat(dfs)
df[['cn', 'title', 'credit']] = df.title.str.split("\.  ", regex=True, expand=True)
df['new_course'] = ~df.title.duplicated()

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)