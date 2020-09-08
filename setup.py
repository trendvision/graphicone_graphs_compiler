from setuptools import setup

setup(
    name='graphicone_graphs_compiler',
    url='https://github.com/trendvision/graphicone_graphs_compiler',
    packages=['graphicone_graphs_compiler'],
    dependency_link=[
        'git+https://github.com/trendvision/graphicone_models.git#egg=graphicone_models',
        'git+https://github.com/trendvision/graphicone_social_relations.git#egg=graphicone_social_relations'
    ],
    install_requires=['sqlalchemy'],
    version='0.1',
    license='TRV',
    description='creation graphs models',
)
