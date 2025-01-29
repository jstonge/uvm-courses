import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import argparse


def main(url_text_file):

    # eyeballed from website
    with open('src/data/uvm-html-urls.txt', 'r') as f:
        url_txt_files = f.readlines()
    
    # Takes a while, as for each year we go over all departments 
    # and we politely wait 1 second between requests.
    course_data = []
    for txt_file in url_txt_files:
        yr = txt_file.stem.split('-')[-2]
        
        with open(txt_file, 'r') as f:
            course_urls = f.readlines()

        print(f"Processing {txt_file} ({yr})")    

        for url in tqdm(course_urls):
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            courseblocks = soup.find_all('div', class_='courseblock')

            for block in courseblocks:
                title = block.find('p', class_='courseblocktitle').get_text(strip=True)
                title = title.replace('\xa0', ' ')
                description = block.find('p', class_='courseblockdesc').get_text(strip=True)

                course_data.append({
                    'url': url,
                    'year': yr,
                    'cat_type': url.split('/')[-4], 
                    'college': url.split('/')[-3],
                    'dept': url.split('/')[-2],
                    'title': title,
                    'description': description
                })

            sleep(1) #politeness
        
    df = pd.DataFrame(course_data)    
    df[['cn', 'title', 'credit']] = df.title.str.split("\.  ", regex=True, expand=True)
    df['new_course'] = ~df.title.duplicated() # probably not the best way to do this
    df.to_parquet('src/data/catalog_html_raw.parquet')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url_text_files", type=str, help="output directory", required=True)
    args = parser.parse_args()
    url_txt_files = args.url_txt_files

    main(url_txt_files)