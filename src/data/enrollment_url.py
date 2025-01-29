from pathlib import Path
import pandas as pd
import sys
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def main():
    # Get all the links directly from page
    base_url="https://serval.uvm.edu/~rgweb/batch/enrollment/"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [base_url+a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".txt")]

    # Wrangle the data a little
    years = [int(str(p).split("_")[-1][:4]) for p in links]
    out = []
    title = ['dept','cn','title','comp numb','sec','lec lab','camp code','max enrollment','current enrollment','start time','end time','days','bldg','room','instructor','credits']
    for yr, link in tqdm(zip(years, links), total=len(links)):
        if yr < 2023:
            inner_out = []
            r = requests.get(link)
            # with open(link) as f:
            for i,line in enumerate(r.text.split("\n")):
                
                
                # first row is title
                if i == 0:
                    line = line.strip("\n").split(",")
                    # title = [e.strip().lower() for e in line]
                    continue
                
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
            df['file'] = str(Path(link).stem)
            out.append(df)

    df = pd.concat(out)
    df.to_parquet("src/data/enrollment_raw.parquet")

if __name__ == "__main__":
    main()