from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.config import APP_NAME
from ui.login_window import LoginWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    window = LoginWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
