from jinja2 import Environment, FileSystemLoader
import os
import json
import shutil
from datetime import datetime

root = os.path.dirname(os.path.abspath(__file__))

# Directories (relative to the repository root) whose subdirectories contain a meta.json
content_dirs = ['notebooks', 'apps', 'papers', 'academic-works', 'blog-articles']

# Public URL of the site (used in canonical links and in the sitemap)
site_url = 'https://filipechagasdev.github.io/FilipeChagasDev/'

# GoatCounter site code (the "xxx" in https://xxx.goatcounter.com). If None, the tracking script is not included.
goatcounter = None

language_codes = {'English': 'en', 'Portuguese': 'pt'}


def read_metadata(content_dir):
    content_path = os.path.join(root, '..', content_dir)
    meta_list = []

    for item_dir in os.listdir(content_path):
        meta_fn = os.path.join(content_path, item_dir, 'meta.json')
        if os.path.exists(meta_fn):
            with open(meta_fn, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            meta['id'] = f'{content_dir}/{item_dir}'
            meta['source_dir'] = os.path.join(content_path, item_dir)
            meta_list.append(meta)

    return meta_list


def render_article_page(env, meta):
    """
    Renders the internal page of a content whose directory has an article.html (the page body).
    The page is written to docs/<content_dir>/<item_dir>/index.html, together with the images directory.
    """
    with open(os.path.join(meta['source_dir'], 'article.html'), 'r', encoding='utf-8') as f:
        content = f.read()

    page_dir = os.path.join(root, meta['id'])
    os.makedirs(page_dir, exist_ok=True)

    images_dir = os.path.join(meta['source_dir'], 'images')
    if os.path.exists(images_dir):
        shutil.copytree(images_dir, os.path.join(page_dir, 'images'), dirs_exist_ok=True)

    template = env.get_template('article.html')
    with open(os.path.join(page_dir, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(template.render(post = meta, content = content, root = '../../', site_url = site_url, goatcounter = goatcounter))


def write_sitemap(pages):
    filename = os.path.join(root, 'sitemap.xml')
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for page in pages:
            fh.write(f'    <url><loc>{site_url}{page}</loc></url>\n')
        fh.write('</urlset>\n')


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

    pages = ['']
    for meta in posts:
        meta.setdefault('contentsubtype', None)
        meta.setdefault('institution', None)
        meta['date_str'] = datetime(meta['date']['year'], meta['date']['month'], meta['date']['day']).strftime('%d-%b-%Y')

        # Contents with an article.html get an internal page; the others link to the external href
        if os.path.exists(os.path.join(meta['source_dir'], 'article.html')):
            meta['link'] = meta['id'] + '/'
            meta['external'] = False
            meta['language_original'] = language_codes.get(meta.get('language'))
            render_article_page(env, meta)
            pages.append(meta['link'])
        else:
            meta['link'] = meta['href']
            meta['external'] = True

    filename = os.path.join(root, 'index.html')
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write(template.render(posts = posts, root = '', goatcounter = goatcounter))

    write_sitemap(pages)
