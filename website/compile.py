from jinja2 import Environment, FileSystemLoader
import os
 
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('index.html')
 
filename = os.path.join(root, 'index.html')
with open(filename, 'w') as fh:
    fh.write(template.render(
        posts = [
            {
                'index': 0,
                'title': 'Seam Carving',
                'intro': 'Seam Carving is an algorithm that reduces the width or height of an image, avoiding distortions in its content. This animation shows the process of reducing the width of an image with Seam Carving: for each pixel of width to be limited, a "minimum energy" vertical path (where there is less variation in brightness) is found and its pixels are removed. In this implementation, the "energy" of the image is calculated as the magnitude of the gradient.',
                'pic': 'https://github.com/FilipeChagasDev/FilipeChagasDev/blob/main/notebooks/seam-carving/output/seam-carving-filipe.gif?raw=true',
                'url': 'https://github.com/FilipeChagasDev/FilipeChagasDev/blob/main/notebooks/seam-carving/seam-carving-filipe.ipynb',
                'content_type': 'Python Notebook',
                'content_topic': 'Image Processing'
            }
        ],
    ))