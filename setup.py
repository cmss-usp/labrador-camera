from setuptools import find_packages, setup, os

def _read_requirements(file_name):
    """
    Returns list of required modules for 'install_requires' parameter. Assumes
    requirements file contains only module lines and comments.
    """
    requirements = []
    with open(os.path.join(file_name)) as f:
        for line in f:
            if not line.startswith('#'):
                requirements.append(line)
    return requirements


INSTALL_REQUIREMENTS = _read_requirements('requirements.txt')


setup(
    name='labrador_camera',
    packages=find_packages(include=['labrador_camera']),
    version='0.1.0',
    description='CMSS labrador_camera',
    author='Geovane',
    license='MIT',
    install_requires=['rich'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
