from setuptools import setup, find_packages

from pkg_resources import Requirement, parse_requirements


def load_requirements(f_name: str) -> list:
    requirements = []
    with open(f_name, 'r') as fp:
        req: Requirement
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                f'{req.project_name}{extras}{req.specs[0][0]}{req.specs[0][1]}'
            )
    return requirements


setup(
    name='dia',
    version='0.0.1',

    packages=find_packages(),
    install_requires=load_requirements('requirements.txt'),
    include_package_data=True,
    package_data={
        '': ['requirements.txt']
    },
    entry_points={
        'console_scripts': [
            'dia=dia.__main__:main'
        ]
    }
)
