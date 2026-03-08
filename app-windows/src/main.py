from __future__ import annotations

import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from app.config import APP_NAME, APP_ORG_DOMAIN, APP_ORG_NAME
from db.session import initialize_database
from ui.app_window import AppWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORG_NAME)
    app.setOrganizationDomain(APP_ORG_DOMAIN)
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)

    initialize_database()

    window = AppWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
