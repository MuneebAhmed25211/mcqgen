from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Muneeb Ahmed',
    author_email='muneebahmad25211@gmail.com',
    install_requires=['openai','langchain','stremlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)