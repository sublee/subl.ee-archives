# -*- coding: utf-8 -*-
from __future__ import print_function

import re

from glob2 import glob


HREF_PATTERN = re.compile('([\'"=])/(?=[^/])')


for filename in glob('*/**/*.html'):
    print(filename)
    with open(filename) as f:
        html = f.read()
    root_path = r'\1' + '../' * (filename.count('/') - 1)
    html = HREF_PATTERN.sub(root_path, html)
    with open(filename + '$', 'w') as f:
        f.write(html)
