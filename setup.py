from distutils.core import setup
import setup_translate


setup(name = 'enigma2-plugin-extensions-tmbd',
		version='8.5.5',
		author='Dorik1972',
		author_email='dima-73@inbox.lv',
		package_dir = {'Extensions.TMBD': 'src'},
		packages=['Extensions.TMBD'],
		package_data={'Extensions.TMBD': ['*.png', 'img/*.png', 'profile/*.py', 'modules/*.py', 'modules/*.whl']},
		description = 'Search the internet bases themoviedb.org/kinopoisk.ru',
		cmdclass = setup_translate.cmdclass,
	)
