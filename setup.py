try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
import distutils.sysconfig
import shutil
import os.path
from os import listdir
import sys
import platform
import urllib.request
import zipfile

exec(open('asterix/version.py').read())

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: C',
    'Programming Language :: C++',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
]

try:
    shutil.rmtree("./build")
except(OSError):
    pass

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
cfg_vars = distutils.sysconfig.get_config_vars()
for key, value in cfg_vars.items():
    if type(value) == str:
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")

# If this is MacOSX set correct deployment target (otherwise compile may fail)
if sys.platform == 'darwin':
    os.environ['MACOSX_DEPLOYMENT_TARGET'] = platform.mac_ver()[0]

ext_include_dirs = ['./asterix/python', './src/asterix', './src/engine']
ext_libraries = []
ext_library_dirs = []
ext_extra_link_args = []

# If this is Windows manually use local expat
if platform.system() == 'Windows':
    if not os.path.exists("expat"):
        urllib.request.urlretrieve("https://www.nuget.org/api/v2/package/expat.v140/2.4.1.1", "expat.zip")
        with zipfile.ZipFile("expat.zip", "r") as zip:
            zip.extractall("expat")
        os.remove("expat.zip")
    ext_include_dirs.append('./expat/build/native/include')
    ext_libraries.append('libexpat')
    ext_library_dirs.append('./expat/build/native/lib/x64/Release')
else:
    ext_extra_link_args.append('-lexpat')

asterix_module = Extension('_asterix',
                           sources=['./src/python/asterix.c',
                                    './src/python/python_wrapper.c',
                                    './src/python/python_parser.cpp',
                                    './src/asterix/AsterixDefinition.cpp',
                                    './src/asterix/AsterixData.cpp',
                                    './src/asterix/Category.cpp',
                                    './src/asterix/DataBlock.cpp',
                                    './src/asterix/DataRecord.cpp',
                                    './src/asterix/DataItem.cpp',
                                    './src/asterix/DataItemBits.cpp',
                                    './src/asterix/DataItemDescription.cpp',
                                    './src/asterix/DataItemFormat.cpp',
                                    './src/asterix/DataItemFormatCompound.cpp',
                                    './src/asterix/DataItemFormatExplicit.cpp',
                                    './src/asterix/DataItemFormatFixed.cpp',
                                    './src/asterix/DataItemFormatRepetitive.cpp',
                                    './src/asterix/DataItemFormatVariable.cpp',
                                    './src/asterix/DataItemFormatBDS.cpp',
                                    './src/asterix/InputParser.cpp',
                                    './src/asterix/Tracer.cpp',
                                    './src/asterix/UAP.cpp',
                                    './src/asterix/UAPItem.cpp',
                                    './src/asterix/Utils.cpp',
                                    './src/asterix/XMLParser.cpp',
                                    ],

                           include_dirs=ext_include_dirs,
                           libraries=ext_libraries,
                           library_dirs=ext_library_dirs,
                           extra_compile_args=['-DPYTHON_WRAPPER'],
                           extra_link_args=ext_extra_link_args)

f = open('README.rst')
try:
    README = f.read()
finally:
    f.close()

config_files = [os.path.join('./asterix/config/', f) for f in listdir('./asterix/config/') if
                os.path.isfile(os.path.join('./asterix/config/', f))]

sample_files = ['./asterix/sample_data/cat048.raw',
                './asterix/sample_data/cat062cat065.raw',
                './asterix/sample_data/cat_034_048.pcap',
                './asterix/sample_data/cat_062_065.pcap']

data_files = []
if platform.system() == 'Windows':
    # data_files.append(('', ['expat/build/native/bin/x64/Release/libexpat.dll'])) # Normal install
    data_files.append(('Lib/site-packages', ['expat/build/native/bin/x64/Release/libexpat.dll'])) # Poetry install

setup(name='asterix_decoder',
      packages=['asterix'],
      version=__version__,
      description="ASTERIX decoder in Python",
      keywords="asterix, eurocontrol, radar, track, croatiacontrol",
      long_description=README,
      ext_modules=[asterix_module],
      data_files = data_files,
      include_package_data=True,
      package_data={'asterix': config_files + sample_files},
      zip_safe=False,
      #       eager_resources = eager_files,
      author="Damir Salantic",
      author_email="damir.salantic@gmail.com",
      download_url="https://github.com/CroatiaControlLtd/asterix",
      license="GPL",
      platforms=['any'],
      url="https://github.com/CroatiaControlLtd/asterix",
      classifiers=CLASSIFIERS,
      )

if platform.system() == 'Windows':
    shutil.rmtree("expat")
