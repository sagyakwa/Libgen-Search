from os.path import join, dirname, abspath

from PyQt5.QtCore import Qt
from qtpy.QtGui import QPalette, QColor

from ._utils import qtpy_version

_STYLESHEET = join(dirname(abspath(__file__)), 'resources/style.qss')
""" str: Main stylesheet. """


def _apply_base_theme(app):
    """ Apply base theme to the application.

        Args:
            app (QApplication): QApplication instance.
    """

    if qtpy_version < (5,):
        app.setStyle('plastique')
    else:
        app.setStyle('Fusion')

    with open(_STYLESHEET) as stylesheet:
        app.setStyleSheet(stylesheet.read())


def dark_mode(app):
    """ Apply Dark Theme to the Qt application instance.

        Args:
            app (QApplication): QApplication instance.
    """

    dark_palette = QPalette()

    # base
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Light, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.Midlight, QColor(90, 90, 90))
    dark_palette.setColor(QPalette.Dark, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.Text, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.BrightText, QColor(180, 180, 180))
    dark_palette.setColor(QPalette.ButtonText, QColor(230, 230, 230))
    dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Link, QColor(56, 252, 196))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)

    # disabled
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText,
                         QColor(127, 127, 127))
    dark_palette.setColor(QPalette.Disabled, QPalette.Highlight,
                         QColor(80, 80, 80))
    dark_palette.setColor(QPalette.Disabled, QPalette.HighlightedText,
                         QColor(127, 127, 127))

    app.setPalette(dark_palette)
    
    _apply_base_theme(app)


def light_mode(app):
    """ Apply Light Theme to the Qt application instance.

        Args:
            app (QApplication): QApplication instance.
    """

    light_palette = QPalette()

    # base
    light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.Light, QColor(180, 180, 180))
    light_palette.setColor(QPalette.Midlight, QColor(200, 200, 200))
    light_palette.setColor(QPalette.Dark, QColor(225, 225, 225))
    light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.BrightText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Base, QColor(237, 237, 237))
    light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    light_palette.setColor(QPalette.Highlight, QColor(76, 163, 224))
    light_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.Link, QColor(0, 162, 232))
    light_palette.setColor(QPalette.AlternateBase, QColor(225, 225, 225))
    light_palette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))

    # disabled
    light_palette.setColor(QPalette.Disabled, QPalette.WindowText,
                         QColor(115, 115, 115))
    light_palette.setColor(QPalette.Disabled, QPalette.Text,
                         QColor(115, 115, 115))
    light_palette.setColor(QPalette.Disabled, QPalette.ButtonText,
                         QColor(115, 115, 115))
    light_palette.setColor(QPalette.Disabled, QPalette.Highlight,
                         QColor(190, 190, 190))
    light_palette.setColor(QPalette.Disabled, QPalette.HighlightedText,
                         QColor(115, 115, 115))

    app.setPalette(light_palette)

    _apply_base_theme(app)
