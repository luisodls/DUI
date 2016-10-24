'''
Containers for widgets related to each step

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
'''

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


from python_qt_bind import *

import os, sys

from params_live_gui_generator import PhilWidget
from dials.command_line.find_spots import phil_scope as phil_scope_find_spots
from dials.command_line.index import phil_scope as phil_scope_index

#from dials.command_line.refine_bravais_settings import phil_scope as phil_scope_refine_br_st

from dials.command_line.refine import phil_scope as phil_scope_refine
from dials.command_line.integrate import phil_scope as phil_scope_integrate

try:
    from dials.command_line.export import phil_scope as phil_scope_export
except:
    from dials.command_line.export_mtz import phil_scope as phil_scope_export

def template_right_side_build(in_str_tmp, dir_path):

    #print "in_str_tmp =", in_str_tmp
    #print "dir_path =", dir_path

    out_str = in_str_tmp + dir_path
    lst_files = os.listdir(str(dir_path))

    for pos, single_char in enumerate(in_str_tmp):
        if( single_char == "." ):
            pos_sep = pos

    left_sd_name = in_str_tmp[:pos_sep]
    #print "left_sd_name =", left_sd_name

    ext_name = in_str_tmp[pos_sep:]
    #print "ext_name =", ext_name


    out_str = left_sd_name

    max_tail_size = int(len(in_str_tmp) / 3)
    #print "max_tail_size =", max_tail_size
    for tail_size in xrange(max_tail_size):
        #print "tail_size =", tail_size
        prev_str = out_str
        pos_to_replase = len(out_str) - tail_size - 1
        #print "pos_to_replase =", pos_to_replase
        for num_char in '0123456789':
            if out_str[pos_to_replase] == num_char:
                out_str = out_str[:pos_to_replase] + '#' + out_str[pos_to_replase + 1:]

        #print "new out_str =", out_str
        if( prev_str == out_str ):
            #print "found non num char"
            break

    out_str = out_str + ext_name
    #print out_str


    return out_str


class ImportPage(QWidget):

    '''
    This stacked widget basically helps the user to browse the input images
    path, there is no auto-generated GUI form Phil parameters in use withing
    this widget.
    '''

    # FIXME when the user enters a path without images dials fails to import
    # but does not raises an error consequently there is no red output in the GUI

    # FIXME study the file:
    # Dxtbx/sweep_filenames.py

    def __init__(self, parent = None):
        super(ImportPage, self).__init__(parent = None)
        self.super_parent = parent # reference across the hole GUI to MyMainDialog

        import_path_group =  QGroupBox("Experiment IMG Directory")
        import_path_layout =  QVBoxLayout()

        self.lin_import_path =   QLineEdit(self)
        import_path_button =  QPushButton(" \n    Find experiment Dir            . \n")
        import_path_button.clicked.connect(self.find_my_img_dir)
        import_path_group.setLayout(import_path_layout)

        import_path_layout.addWidget(import_path_button)
        import_path_layout.addWidget(self.lin_import_path)


        template_grp =  QGroupBox("Template ")
        template_vbox =  QHBoxLayout()
        self.templ_lin =   QLineEdit(self)
        self.templ_lin.setText("Generated Template =")
        template_vbox.addWidget(self.templ_lin)
        template_grp.setLayout(template_vbox)


        mainLayout =  QVBoxLayout()
        mainLayout.addWidget(import_path_group)
        mainLayout.addWidget(template_grp)

        big_layout =  QHBoxLayout()
        big_layout.addLayout(mainLayout)

        self.setLayout(big_layout)
        self.show()


    def find_my_img_dir(self, event = None):

        selected_file_path = str( QFileDialog.getOpenFileName(self, "Open IMG Dir"))
        print "[ file path selected ] =", selected_file_path

        if( selected_file_path ):
            for pos, single_char in enumerate(selected_file_path):
                if( single_char == "/" or single_char == "\\" ):
                    pos_sep = pos

            dir_name = selected_file_path[:pos_sep]
            if( dir_name[0:3] == "(u\'" ):
                print "dir_name[0:3] == \"(u\'\""
                dir_name = dir_name[3:]

            print "dir_name(final) =", dir_name

            templ_str_tmp = selected_file_path[pos_sep:]
            #print "templ_str_tmp =", templ_str_tmp

            templ_r_side = template_right_side_build(templ_str_tmp, dir_name)

            templ_str_final = dir_name + templ_r_side

            self.lin_import_path.setText(dir_name)
            self.templ_lin.setText(templ_str_final)

        else:
            print "Failed to pick dir"

class RefineBrvPage(QWidget):

    def __init__(self, parent = None):
        super(RefineBrvPage, self).__init__(parent = None)
        self.super_parent = parent  # reference across the hole GUI to MyMainDialog
        ops_layout =  QVBoxLayout()
        #ops_layout.setMargin(0)    # this does NOT work in PySide
        ops_layout.setContentsMargins(QMargins(0,0,0,0))
        ops_layout.setSpacing(0)

        lst_ops = []
        for lin in xrange(5):
            labl = str("op #" + str(lin) + "Pick me")
            new_op = QPushButton(labl)
            ops_layout.addWidget(new_op)
            lst_ops.append(new_op)

        big_layout =  QVBoxLayout()
        big_layout.addWidget(QLabel("Select option "))
        big_layout.addLayout(ops_layout)
        big_layout.addWidget(QLabel("option Selected ="))

        self.setLayout(big_layout)
        self.show()

class ParamMainWidget( QWidget):
    def __init__(self, phl_obj = None, parent = None):
        super(ParamMainWidget, self).__init__()
        self.super_parent = parent # reference across the hole GUI to MyMainDialog
        self.scrollable_widget = PhilWidget(phl_obj, parent = self)
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.scrollable_widget)
        hbox =  QHBoxLayout()
        hbox.addWidget(scrollArea)
        self.setLayout(hbox)
        self.show()

    def update_lin_txt(self, str_path, str_value):
        print "running command = {", str_path, "=", str_value,"}"


class StepList(object):


    lst_lablel = [
                  " import",
                  "find spots",
                  "index",
                  "refine bravais settings",
                  #"reindex",
                  "refine",
                  "integrate"
                  #,"export"
                  ]

    lst_commands = [
                    "import",
                    "find_spots",
                    "index",
                    "refine_bravais_settings",
                    #"reindex",
                    "refine",
                    "integrate"
                    #,"export"
                   ]

    def __init__(self, parent = None):
        self.super_parent = parent
        self.lst_widg  = [
                          ImportPage(parent = self),
                          ParamMainWidget(phl_obj = phil_scope_find_spots, parent = self),
                          ParamMainWidget(phl_obj = phil_scope_index, parent = self),
                          RefineBrvPage(parent = self),
                          ParamMainWidget(phl_obj = phil_scope_refine, parent = self),
                          ParamMainWidget(phl_obj = phil_scope_integrate, parent = self)
                         ]

        idials_path = os.environ["IDIALS_PATH"]
        print "idials_path =", idials_path

        lst_icons_path = []

        lst_icons_path.append(str(idials_path + "/resources/import.png"))
        lst_icons_path.append(str(idials_path + "/resources/find_spots.png"))
        lst_icons_path.append(str(idials_path + "/resources/index.png"))
        #lst_icons_path.append(str(idials_path + "/resources/refine_v_sets.png"))
        lst_icons_path.append(str(idials_path + "/resources/reindex.png"))
        lst_icons_path.append(str(idials_path + "/resources/refine.png"))
        lst_icons_path.append(str(idials_path + "/resources/integrate.png"))
        #lst_icons_path.append(str(idials_path + "/resources/export.png"))

        self.lst_icons = []
        for my_icon_path in lst_icons_path:
            self.lst_icons.append(QIcon(my_icon_path))
            print "attempting to append:", my_icon_path

    def __call__(self):
        return self.lst_lablel, self.lst_widg, self.lst_icons, self.lst_commands



class importOuterWidget( QWidget):
    def __init__(self, parent = None):
        super(importOuterWidget, self).__init__(parent)

        import_widget = ImportPage(self)
        vbox =  QVBoxLayout(self)
        vbox.addWidget(import_widget)
        self.setLayout(vbox)
        self.show()



if __name__ == '__main__':
    app =  QApplication(sys.argv)
    ex = importOuterWidget()
    sys.exit(app.exec_())


