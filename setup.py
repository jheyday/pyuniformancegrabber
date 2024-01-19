from setuptools import setup

setup(name='pyuniformancegrabber',
      version='0.2',
      description='Access honeywell phd via .netframework wrapper for PHDAPINET.DLL',
      url='https://github.com/jheyday/pyuniformancegrabber',
      author='jheyday',
      author_email='not@anemail.com',
      license='MIT',
      packages=['pyuniformancegrabber'],
      install_requires=[
          'pandas',
          'lxml',
          
      ],
      zip_safe=False,
      include_package_data=True
)