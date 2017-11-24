from setuptools import setup
setup(name='dui_test',
      version='1.0',
      license="GPL 2.0",
      description="Dials User Interface, pre - release Test",
      author='Luis Fuentes-Montero (Luiso)',
      author_email='luis.fuentes-montero@diamond.ac.uk',
      url='none yet',
      platforms='GNU/Linux & Mac OS',

      packages=['mini_idials_w_GUI', 'mini_idials_w_GUI.outputs_n_viewers'],
      data_files=[('logos_01', ['mini_idials_w_GUI/DIALS_Logo_smaller_centred_grayed.png',
                             'mini_idials_w_GUI/DIALS_Logo_smaller_centred.png',
                             'mini_idials_w_GUI/find_spots_grayed.png',
                             'mini_idials_w_GUI/find_spots.png',
                             'mini_idials_w_GUI/import_grayed.png',
                             'mini_idials_w_GUI/import.png',
                             'mini_idials_w_GUI/index_grayed.png',
                             'mini_idials_w_GUI/index.png',
                             'mini_idials_w_GUI/integrate_grayed.png',
                             'mini_idials_w_GUI/integrate.png',
                             'mini_idials_w_GUI/refine_grayed.png',
                             'mini_idials_w_GUI/refine.png',
                             'mini_idials_w_GUI/reindex_grayed.png',
                             'mini_idials_w_GUI/reindex.png',
                             'mini_idials_w_GUI/re_try_grayed.png',
                             'mini_idials_w_GUI/re_try.png',
                             'mini_idials_w_GUI/stop_grayed.png',
                             'mini_idials_w_GUI/stop.png'])],
      entry_points={'console_scripts':['dui=mini_idials_w_GUI.main_dui:main']},
     )

