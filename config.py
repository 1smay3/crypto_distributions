import os


base_url ="https://financialmodelingprep.com/api/"
version  = "v3/"

api_key = "6a7bfe0b2162048feb12ab86dbd15631"

# Add slash as os.join can only interpret '/' at the start of a path if it is the root of the directory
project_root = os.path.abspath(os.path.dirname(__file__)) + "/"
data_root = os.path.abspath(os.path.dirname(__file__)) + "/data/data_store/"

print(data_root)