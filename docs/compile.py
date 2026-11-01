from jinja2 import Environment, FileSystemLoader
import os
import json
from datetime import datetime

root = os.path.dirname(os.path.abspath(__file__))

# Directories (relative to the repository root) whose subdirectories contain a meta.json
content_dirs = ['notebooks', 'apps', 'papers', 'academic-works']


def read_metadata(content_dir):
    content_dir = os.path.join(root, '..', content_dir)
    meta_list = []

    for item_dir in os.listdir(content_dir):
        meta_fn = os.path.join(content_dir, item_dir, 'meta.json')
        if os.path.exists(meta_fn):
            with open(meta_fn, 'r', encoding='utf-8') as f:
                meta_list.append(json.load(f))

    return meta_list


if __name__ == '__main__':
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('index.html')

    posts = []
    for content_dir in content_dirs:
        posts = posts + read_metadata(content_dir)

    posts.sort(
            key=lambda meta: (meta['relevance'], datetime(meta['date']['year'], meta['date']['month'], meta['date']['day'])),
            reverse=True
        )

    for meta in posts:
        meta.setdefault('contentsubtype', None)
        meta.setdefault('institution', None)
        meta['date_str'] = datetime(meta['date']['year'], meta['date']['month'], meta['date']['day']).strftime('%d-%b-%Y')

    filename = os.path.join(root, 'index.html')
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write(template.render(posts = posts))
