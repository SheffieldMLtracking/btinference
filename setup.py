from distutils.core import setup
setup(
  name = 'btinference',
  packages = ['btinference'],
  version = '1.0',
  description = 'This computes the 3d path of the bee.',
  author = 'Mike Smith',
  author_email = 'm.t.smith@sheffield.ac.uk',
  url = 'https://github.com/SheffieldMLtracking/btinference.git',
  download_url = 'https://github.com/SheffieldMLtracking/btinference.git',
  keywords = ['3d','path','bee','flight','cameras','pose','position'],
  classifiers = [],
  install_requires=['numpy'],
  scripts=['bin/btinference'],
)
