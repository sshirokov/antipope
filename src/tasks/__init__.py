import os, re, inspect

pwd = os.path.dirname(inspect.currentframe().f_code.co_filename)
tasklist = [f.split('.')[0] for f in
         filter(lambda f: re.search('^[^_]\w+\\.py$', f), os.listdir(pwd))]
