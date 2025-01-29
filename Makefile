FRAMEWORK_DIR=$(realpath ./src)
DATA_DIR_OBS=$(FRAMEWORK_DIR)/data
ANNOT_DIR = $(DATA_DIR_OBS)/annotated_m_split_courses
UVM_NETID=jstonge1

.PHONY: parsed-data html-data enrollement-data

# Get the raw data

parsed-data: # -> annotated_data.parquet
	mkdir -p $(DATA_DIR_OBS)/annotated_m_split_courses
	rsync -av $(UVM_NETID)@vacc-user1.uvm.edu:"/netfiles/compethicslab/cc/annotated_m_split_courses/0155zta11_ug_20*" $(ANNOT_DIR)/
	python $(DATA_DIR_OBS)/uvm_parse_repair.py 

# Takes a little while.
html-data: # -> catalog_html_raw.parquet
	python $(DATA_DIR_OBS)/catalog_html_url.py -u $(DATA_DIR_OBS)/uvm-html-urls.txt

# No url input, we grab directly from the website
enrollement-data: # -> enrollment_raw.parquet
	python $(DATA_DIR_OBS)/enrollment_url.py


# Once the raw data is obtained, 
# use `npm run dev` will lauch the data app