import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='flespi-gateway',
      version='0.0.1',
      description='The python wrapper of a gateway rest API of a flespi platform.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/vlavrik/flespi-gateway',
      author='Dr. Vladimir Lavrik',
      author_email='lavrikvladimir@gmail.com',
      license='BSD 3-Clause "New" or "Revised" License',
      packages=setuptools.find_packages(),
      zip_safe=False,
      python_requires='>=3.8')
