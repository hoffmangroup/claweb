from setuptools import find_packages
from setuptools import setup


def post_install_cleaning():
    """Remove dist, eggs, and build directory after install"""

    import shutil
    import glob
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree(glob.glob('*.egg-info')[0])


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="claweb",
    version="0.0.1",
    author="mmendez12",
    author_email="mickael.mendez@mail.utoronto.ca",
    description="Generate website summary for the Cell Lineage Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mmendez12/claweb",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/claweb_make_website.py'], install_requires=['pandas'],
    entry_points = {
        'console_scripts': [
            'claweb-make-gac=claweb.f5clonto_helper.parse_20170801:cli_make_gac',
            'claweb-make-graph-coord=claweb.f5clonto_helper.make_ontoviewer_coords:cli_make_graph_coord',
            'claweb-make-updown-count=claweb.f5clonto_helper.up_down_neither_count:cli_make_updown_count',
            'claweb-plot-ontology=claweb.f5clonto_helper.ontoviewer:cli_plot_ontology',
            'claweb-make-website=claweb.controller.master:cli_make_website',
            'claweb-make-website-comparisons=claweb.controller.master:cli_make_website_comparisons',
        ]
    },
    include_package_data=True
)

post_install_cleaning()
