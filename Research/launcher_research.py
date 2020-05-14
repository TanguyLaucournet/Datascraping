

import pandas as pd
from requests import get
from bs4 import BeautifulSoup 
import runpy

runpy.run_path(path_name='scraping_inwara.py')

runpy.run_path(path_name='scraping_cbinsight.py')
