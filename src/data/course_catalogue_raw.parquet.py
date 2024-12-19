from pathlib import Path
import pandas as pd
import sys
import pyarrow as pa
import pyarrow.parquet as pq


# reading the files is finicky; bouuh to CSV files.
paths = [_ for _ in Path("src/data/raw-data").glob("*txt") if str(_).split("/")[-1] != "all_links.txt"]
years = [int(str(p).split("_")[-1][:4]) for p in paths]
out = []
title = ['dept','cn','title','comp numb','sec','lec lab','camp code','max enrollment','current enrollment','start time','end time','days','bldg','room','instructor','credits']
for yr, path in zip(years, paths):
    if yr < 2023:
        inner_out = []
        with open(path) as f:
            for i,line in enumerate(f.readlines()):
                # first row is title
                if i == 0:
                    line = line.strip("\n").split(",")
                    # title = [e.strip().lower() for e in line]
                    continue
                # break
                split_line = line.strip("\n").split("\",")
                if len(split_line) == 1:
                    split_line = line.strip("\n").split(",")
                    
                if len(split_line) != len(title):
                    # print((path, i, len(split_line), line))
                    # not great solution; often this is because 
                    # instructor have a comma in their name.
                    # There probably is an easier way to do that.
                    split_line = split_line[:15] + split_line[-1:]
                    
                split_line = [e.strip("\"").strip() for e in split_line]
                
                inner_out.append(split_line)
        
        df=pd.DataFrame(inner_out, columns=title)
        df['year'] = yr
        df['file'] = str(path)
        out.append(df)

df = pd.concat(out)

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)