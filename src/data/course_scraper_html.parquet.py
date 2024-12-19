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

# with open("src/data/html-catalog/urls-2015-2016.txt") as f:
#     course_urls = f.read().splitlines()

# with open("src/data/html-catalog/urls-2016-2017.txt") as f:
#     course_urls = f.read().splitlines()

# with open("src/data/html-catalog/urls-2017-2018.txt") as f:
#     course_urls = f.read().splitlines()

with open("src/data/html-catalog/urls-2023-2024.txt") as f:
    course_urls = f.read().splitlines()


# ----

# course_data = []

# for url in course_urls:
#     # url=course_urls[0]
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
# df.to_csv("src/data/html-catalog/2023-24-html-catalog.csv", index=False)


df2014 = pd.read_csv("src/data/html-catalog/2014-15-html-catalog.csv")
df2014['year'] = 2014
df2015 = pd.read_csv("src/data/html-catalog/2015-16-html-catalog.csv")
df2015['year'] = 2015
df2016 = pd.read_csv("src/data/html-catalog/2016-17-html-catalog.csv")
df2016['year'] = 2016
df2017 = pd.read_csv("src/data/html-catalog/2017-18-html-catalog.csv")
df2017['year'] = 2017
df2023 = pd.read_csv("src/data/html-catalog/2023-24-html-catalog.csv")
df2023['year'] = 2023

df = pd.concat([df2014, df2015, df2016, df2017, df2023])

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)