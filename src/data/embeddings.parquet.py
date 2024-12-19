
import hdbscan 
import umap
import pandas as pd
from sentence_transformers import SentenceTransformer
import pyarrow as pa
import pyarrow.parquet as pq
import sys
from nltk.tokenize import word_tokenize

dfs = []
for yr in range(2014, 2018):
    d=pd.read_csv(f"src/data/html-catalog/{yr}-{str(yr+1)[-2:]}-html-catalog.csv")
    d['year'] = yr
    dfs.append(d)

d=pd.concat(dfs, axis=0)
d['toks'] = d.description.map(word_tokenize)
d['wc'] = d.toks.map(len)
d['description'] = d.description.str.replace("Prerequisite.*", "", case=False, regex=True)
d = d[d.wc > 10]
d.reset_index(drop=True, inplace=True)

model = SentenceTransformer("all-MiniLM-L6-v2") 
embeddings = model.encode(d.description.astype(str)) 

# similarities = model.similarity(embeddings, embeddings)
# dfsim = pd.DataFrame(similarities).round(3)
# idx_phi = d[d.dept == 'philosophy'].index
# dfsim_phi = dfsim.iloc[idx_phi, idx_phi].reset_index(names='source')
# long_df = pd.melt(dfsim_phi, id_vars=['source'], var_name='target', value_name='similarity')
# long_df.to_parquet("src/data/sim_matrix_phi.parquet")


mapper = umap.UMAP().fit(embeddings)
clusterer = hdbscan.HDBSCAN() 
clusterer.fit(mapper.embedding_) 
dclus = pd.DataFrame(mapper.embedding_, columns=['x','y']).assign(cluster=clusterer.labels_)

df = pd.concat([dclus, d], axis=1)

# Write DataFrame to a temporary file-like object
buf = pa.BufferOutputStream()   
table = pa.Table.from_pandas(df)
pq.write_table(table, buf, compression="snappy")

# Get the buffer as a bytes object
buf_bytes = buf.getvalue().to_pybytes()

# Write the bytes to standard output
sys.stdout.buffer.write(buf_bytes)