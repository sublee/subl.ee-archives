# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import date
import os
import re
import subprocess

import click


@click.group()
def cli():
    pass


@cli.command()
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


@cli.command()
@click.argument('src_repo', type=click.Path(file_okay=False, exists=True))
def index(src_repo):
    repo = os.path.dirname(os.path.abspath(__file__))
    commits = []
    for filename in os.listdir(repo):
        if not os.path.isdir(filename):
            continue
        elif len(filename) != 7:
            continue
        commit = filename
        time = int(subprocess.check_output([
            'git', '-C', src_repo, '--no-pager',
            'show', '-s', '--date=unix', '--format=%ad', commit,
        ]))
        commits.append((time, commit))
    commits.sort(reverse=True)
    print('<ul>')
    for time, commit in commits:
        print('  <li><a href="{commit}">{commit}</a> ({date:%Y-%m-%d})</li>'
              ''.format(date=date.fromtimestamp(time), commit=commit))
    print('</ul>')


if __name__ == '__main__':
    cli()
