import pandas as pd
import sys
import pyarrow as pa
import pyarrow.parquet as pq

df = pd.read_csv("src/data/annotated_data.parquet")

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)