from setuptools import setup

setup(
    name='graphicone_graphs_compiler',
    url='https://github.com/trendvision/graphicone_graphs_compiler',
    packages=['graphicone_graphs_compiler'],
    install_requires=[
        'sqlalchemy'
        'graphicone_models @ git+https://github.com/trendvision/graphicone_models.git#egg=graphicone_models',
        'graphicone_social_relations @ git+https://github.com/trendvision/graphicone_social_relations.git#egg=graphicone_social_relations'
    ],
    version='0.1.1',
    license='TRV',
    description='creation graphs models',
)
