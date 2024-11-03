from jinja2 import Environment, FileSystemLoader
import os
import json
from datetime import datetime

root = os.path.dirname(os.path.abspath(__file__))

def read_notebooks_metadata():
    notebooks_dir = os.path.join(root, '..', 'notebooks')
    notebooks_meta_list = []

    for notebook_dir in os.listdir(notebooks_dir):
        meta_fn = os.path.join(notebooks_dir, notebook_dir, 'meta.json')
        if os.path.exists(meta_fn):
            with open(meta_fn, 'r') as f:
                notebooks_meta_list.append(json.load(f))

    return notebooks_meta_list

if __name__ == '__main__':
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader = FileSystemLoader(templates_dir))
    template = env.get_template('index.html')
    
    posts = read_notebooks_metadata()
    
    posts.sort(
            key=lambda meta: (meta['relevance'], datetime(meta['date']['year'], meta['date']['month'], meta['date']['day']))
        )
    
    for meta in posts:
        meta['date_str'] = datetime(meta['date']['year'], meta['date']['month'], meta['date']['day']).strftime('%d-%b-%Y')

    filename = os.path.join(root, 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(posts = posts))