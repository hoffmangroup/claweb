from setuptools import find_packages
from setuptools import setup


def post_install_cleaning():
    """Remove dist, eggs, and build directory after install"""

    import shutil, glob
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree(glob.glob('*.egg-info')[0])


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycomp_mvc",
    version="0.0.1",
    author="mmendez12",
    author_email="mickael.mendez@mail.utoronto.ca",
    description="Generate website summary for the Cell Lineage Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmendez12/pycomp_mvc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/pycomp_make_website.py'], install_requires=['pandas'],
    entry_points = {
        'console_scripts': [
            'pycomp-make-gac=pycomp.f5clonto_helper.parse_20170801:main',
            'pycomp-make-graph-coord=pycomp.f5clonto_helper.make_ontoviewer_coords:main',
            'pycomp-make-updown-count=pycomp.f5clonto_helper.up_down_neither_count:main',
            'pycomp-plot-ontology=pycomp.f5clonto_helper.ontoviewer:main',
        ]
    },
    include_package_data=True
)

post_install_cleaning()
