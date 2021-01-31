import sys
import os
from PyQt5 import QtCore, QtWidgets
import design
from glitch_this.glitch_this import ImageGlitcher

VALUE_ERROR = 'VALUE_ERROR'
EMPTY_ERROR = 'EMPTY_ERROR'

class ExampleApp(QtWidgets.QMainWindow, design.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.importBtm.clicked.connect(self.browse_file)
        self.runBtm.clicked.connect(self.run_glitch)

    def browse_file(self):
        self.nameLabel.clear()
        self.pathLabel.clear()
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Set file")

        if file:
            filepath = os.path.normpath(file[0])
            filename = filepath.split(os.sep)
            self.pathLabel.setText(filepath)
            self.nameLabel.setText(filename[-1])

    def run_glitch(self):
        glitch_value = self.lineEdit.text()
        path = self.pathLabel.text()
        name = self.nameLabel.text()
        if glitch_value and path and name:
            try:
                x = float(glitch_value)
                if x < 0.1 or x > 10:
                    self.create_modal(VALUE_ERROR)
                else:
                    self.create_clitch_file()
            except:
                print('GF')
                #self.create_modal(VALUE_ERROR)
        else:
            self.create_modal(EMPTY_ERROR)

    def create_modal(self, modal_type):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Error")
        dlg.label = QtWidgets.QLabel(dlg)
        dlg.label.setGeometry(QtCore.QRect(20, 20, 200, 50))
        dlg.label.setObjectName("label")
        if modal_type == EMPTY_ERROR:
            dlg.label.setText("Import files or glitch quality not found")
        elif modal_type == VALUE_ERROR:
            dlg.label.setGeometry(QtCore.QRect(20, 20, 370, 50))
            dlg.label.setText("Glitch quality not a number or does not include values in between 0.1 and 10")
        else:
            dlg.label.setText("Something went wrong")
        dlg.exec_()

    def create_clitch_file(self):
        path = self.pathLabel.text()
        level = float(self.lineEdit.text())
        glitcher = ImageGlitcher()
        input_gif = False
        if not input_gif:
            glitch_img = glitcher.glitch_image(path, level,
                                               glitch_change=0.0,
                                               cycle=True,
                                               seed=None,
                                               gif=False,
                                               frames=23,
                                               step=1)
        else:
            glitch_img = glitcher.glitch_gif(path, level,
                                               glitch_change=0.0,
                                               cycle=True,
                                               seed=None,
                                               gif=True,
                                               frames=23,
                                               step=1)
            input_gif = True
            # Set args.duration to src_duration * relative duration, if one was given
            duration = 200

        if not input_gif:
            glitch_img.save(path, compress_level=3)
        else:
            glitch_img[0].save(path,
                               format='GIF',
                               append_images=glitch_img[1:],
                               save_all=True,
                               duration=duration,
                               loop=0,
                               compress_level=3)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()