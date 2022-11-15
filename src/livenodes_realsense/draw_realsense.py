import cv2
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

from .ports import Ports_data, Ports_empty
from livenodes.viewer import View_QT

class Draw_realsense(View_QT):
    """
    Draw all the first two received data channels as heat plot.
    
    Time is represented via alpha values. The most current point is opaque the furthest point away is at 10% alpha.

    Draws on a qt canvas.
    """

    ports_in = Ports_data()
    ports_out = Ports_empty()

    category = "Draw"
    description = ""

    example_init = {
        "name": "Video Render",
    }

    def __init__(self,
                name="Video Render",
                 **kwargs):
        super().__init__(name=name, **kwargs)
        self.name = name

    def _settings(self):
        """
        Get the Nodes setup settings.
        Primarily used for serialization from json files.
        """
        return { \
            "name": self.name
        }

    def _init_draw(self, parent):
        """
        Visualize video framewise.
        """
        self.frame_label = QLabel()

        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame_label)
        self.frame_label.setAlignment(QtCore.Qt.AlignCenter)

        def update(data=[]):
            playback_colormap = self.convert_cv_to_qt(data[0])
            self.frame_label.setPixmap(playback_colormap)

        return update

    # data should follow the (batch/file, time, channel) format
    def process(self, data,  **kwargs):  
        self._emit_draw(data=data)

    def convert_cv_to_qt(self, cv_img):
        """
        Convert from an opencv image to QPixmap.
        Code source: https://github.com/docPhil99/opencvQtdemo/blob/master/staticLabel2.py
        """
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

        return QPixmap.fromImage(convert_to_Qt_format)