# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import re

import click


@click.command()
@click.argument('dest', type=click.Path(file_okay=False, exists=True))
def preserve(dest):
    for dirname, __, filenames in os.walk(dest):
        for filename in filenames:
            path = os.path.join(dirname, filename)
            with open(path) as f:
                data = f.read()
            if path.endswith('.html'):
                rel_root = '../' * (path.count('/') - 1)
                data = re.sub('([\'"])/(?=[^\'"/])', r'\1' + rel_root, data)
                data = data.replace('"/"', '"%s"' % rel_root)
            if filename.endswith('themes/index.html'):
                data = data.replace('"/"+\'#\'', '"../"+\'#\'')
            with open(path, 'w') as f:
                f.write(data)


if __name__ == '__main__':
    preserve()
