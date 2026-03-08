from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QFileDialog,
    QGridLayout,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStyledItemDelegate,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from services.camera_service import CameraOption, CameraService
from services.draft_service import DraftService
from services.employee_service import EmployeeRecord, EmployeeService
from services.settings_service import AppSettings, SettingsService
from ui.common import ScreenContainer, app_stylesheet, apply_window_icon, build_footer, build_logo_label, create_card, create_mode_button, create_page_header, create_split_header, set_logo_height



class NoWheelComboBox(QComboBox):
    def wheelEvent(self, event) -> None:  # type: ignore[override]
        event.ignore()


class CenteredTableDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index) -> None:  # type: ignore[override]
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class LoginPage(QWidget):
    def __init__(self, window: "AppWindow") -> None:
        super().__init__()
        self.window = window

        container = ScreenContainer()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(container)

        card, card_layout = create_card()
        self.card = card
        self.card.setMaximumWidth(1360)
        self.card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        card_layout.setSpacing(20)

        input_shell = QFrame()
        input_shell.setObjectName("heroInputShell")
        input_shell.setFixedHeight(96)
        input_layout = QVBoxLayout(input_shell)
        input_layout.setContentsMargins(18, 10, 18, 10)
        input_layout.setSpacing(2)

        prompt_label = QLabel("請輸入您的員工號碼")
        prompt_label.setObjectName("heroInputHint")
        prompt_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.employee_id_input = QLineEdit()
        self.employee_id_input.setObjectName("heroInput")
        self.employee_id_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.employee_id_input.textChanged.connect(self.handle_employee_id_changed)
        self.employee_id_input.returnPressed.connect(self.handle_enter)

        input_layout.addWidget(prompt_label)
        input_layout.addWidget(self.employee_id_input)

        self.enter_button = QPushButton("請點我開始工作")
        self.enter_button.setMinimumHeight(78)
        self.enter_button.clicked.connect(self.handle_enter)

        self.helper_label = QLabel("若查不到員工，請到系統設定編輯或匯入員工資料。")
        self.helper_label.setObjectName("employeeStatus")
        self.helper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.helper_label.setWordWrap(True)
        self.helper_label.setMinimumHeight(28)

        settings_row = QWidget()
        settings_layout = QVBoxLayout(settings_row)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(0)
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(lambda _checked=False: self.window.show_settings("login"))
        settings_layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignLeft)

        logo_wrap = QWidget()
        self.logo_wrap = logo_wrap
        logo_wrap.setFixedHeight(320)
        logo_layout = QVBoxLayout(logo_wrap)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)
        logo_layout.addStretch(1)
        self.logo_label = build_logo_label(300)
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        logo_layout.addStretch(1)

        card_layout.addWidget(input_shell)
        card_layout.addWidget(self.enter_button)
        card_layout.addWidget(self.helper_label)
        card_layout.addWidget(settings_row)

        container.layout.addSpacing(12)
        container.layout.addWidget(logo_wrap, 0, Qt.AlignmentFlag.AlignHCenter)
        container.layout.addWidget(card, 0, Qt.AlignmentFlag.AlignHCenter)
        container.layout.addStretch(1)
        container.layout.addWidget(build_footer())
        QTimer.singleShot(0, self._apply_responsive_layout)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        QTimer.singleShot(0, self._apply_responsive_layout)

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        height = max(self.height(), self.window.height(), 1)
        width = max(self.width(), self.window.width(), 1)
        logo_wrap_height = max(240, min(320, int(height * 0.20)))
        logo_height = max(230, min(320, int(height * 0.18)))
        card_width = max(900, min(1360, width - 80))
        input_height = 82 if height < 900 else 92 if height < 1200 else 100

        self.logo_wrap.setFixedHeight(logo_wrap_height)
        set_logo_height(self.logo_label, logo_height)
        self.card.setMaximumWidth(card_width)
        self.input_shell.setFixedHeight(input_height)

    def reset(self) -> None:
        self.employee_id_input.setFocus()

    def handle_employee_id_changed(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        employee = self.window.employee_service.find_by_id(employee_id)
        self.window.current_employee = employee

        if employee is None:
            if employee_id:
                self.enter_button.setText("查不到員工，請先修正資料")
                self.helper_label.setText("查不到員工，請到系統設定編輯或匯入員工資料。")
            else:
                self.enter_button.setText("請點我開始工作")
                self.helper_label.setText("若查不到員工，請到系統設定編輯或匯入員工資料。")
            return

        self.enter_button.setText(f"歡迎尊貴的 {employee.employee_id} {employee.name}，請點我開始工作")
        self.helper_label.setText("")

    def handle_enter(self) -> None:
        employee_id = self.employee_id_input.text().strip()
        if not employee_id:
            QMessageBox.warning(self, "資料不足", "請先輸入員工編號。")
            return

        employee = self.window.employee_service.find_by_id(employee_id)
        if employee is None:
            QMessageBox.warning(self, "查無員工", "找不到這個員工編號，請先到系統設定匯入或編輯員工資料。")
            return

        self.window.current_employee = employee
        self.window.show_mode(employee)


class ModeSelectPage(QWidget):
    def __init__(self, window: "AppWindow") -> None:
        super().__init__()
        self.window = window
        self.cameras: list[CameraOption] = []

        container = ScreenContainer()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(container)

        container.layout.addWidget(create_split_header("選擇作業模式", "請直接選擇要進行的作業。"))

        card, card_layout = create_card()
        self.card = card
        self.card.setMaximumWidth(1360)
        self.card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        card_layout.setSpacing(20)

        self.operator_label = QLabel()
        self.operator_label.setObjectName("cameraStatus")
        card_layout.addWidget(self.operator_label)

        mode_row = QHBoxLayout()
        mode_row.setSpacing(20)
        shipment_button = create_mode_button("出貨作業")
        shipment_button.clicked.connect(lambda _checked=False: self.window.show_workflow("shipment"))
        repair_button = create_mode_button("維修收貨")
        repair_button.clicked.connect(lambda _checked=False: self.window.show_workflow("repair"))
        return_button = create_mode_button("退貨收貨")
        return_button.clicked.connect(lambda _checked=False: self.window.show_workflow("return"))
        mode_row.addWidget(shipment_button, 1)
        mode_row.addWidget(repair_button, 1)
        mode_row.addWidget(return_button, 1)
        card_layout.addLayout(mode_row, 1)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)
        left_actions = QHBoxLayout()
        left_actions.setSpacing(12)
        settings_button = QPushButton("系統設定")
        settings_button.setObjectName("secondaryButton")
        settings_button.clicked.connect(lambda _checked=False: self.window.show_settings("mode"))
        back_button = QPushButton("返回登入")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(lambda _checked=False: self.window.show_login())
        left_actions.addWidget(settings_button)
        left_actions.addWidget(back_button)
        left_actions_widget = QWidget()
        left_actions_widget.setLayout(left_actions)

        camera_wrap = QWidget()
        camera_layout = QHBoxLayout(camera_wrap)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(10)
        camera_label = QLabel("作業相機")
        camera_label.setObjectName("fieldLabel")
        self.camera_combo = NoWheelComboBox()
        self.camera_combo.setMinimumWidth(320)
        self.camera_combo.setMinimumHeight(48)
        self.camera_combo.currentIndexChanged.connect(self.persist_selected_camera)
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_combo)

        bottom_row.addWidget(left_actions_widget)
        bottom_row.addStretch(1)
        bottom_row.addWidget(camera_wrap)
        card_layout.addLayout(bottom_row)

        container.layout.addWidget(card, 1)
        container.layout.addWidget(build_footer())

    def refresh(self) -> None:
        employee = self.window.current_employee
        if employee is None:
            self.operator_label.setText("目前尚未帶入操作人員。")
        else:
            self.operator_label.setText(f"目前操作人員：{employee.employee_id} / {employee.name}")
        self.refresh_camera_options()

    def refresh_camera_options(self) -> None:
        self.cameras = self.window.camera_service.list_cameras()
        selected_camera = self.window.camera_service.get_selected_camera(self.cameras)
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        if not self.cameras:
            self.camera_combo.addItem("沒有偵測到相機", "")
            self.camera_combo.setEnabled(False)
        else:
            self.camera_combo.setEnabled(True)
            for camera in self.cameras:
                self.camera_combo.addItem(camera.name, camera.id)
            selected_index = 0
            if selected_camera is not None:
                for index, camera in enumerate(self.cameras):
                    if camera.id == selected_camera.id:
                        selected_index = index
                        break
            self.camera_combo.setCurrentIndex(selected_index)
        self.camera_combo.blockSignals(False)

    def persist_selected_camera(self) -> None:
        camera_id = str(self.camera_combo.currentData())
        if camera_id:
            self.window.camera_service.save_selected_camera_id(camera_id)

    def selected_camera_name(self) -> str:
        camera_id = str(self.camera_combo.currentData())
        for camera in self.cameras:
            if camera.id == camera_id:
                return camera.name
        return "尚未選擇"


class SettingsPage(QWidget):
    def __init__(self, window: "AppWindow") -> None:
        super().__init__()
        self.window = window

        container = ScreenContainer()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(container)

        top_bar = QHBoxLayout()
        back_button = QPushButton("返回")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(lambda _checked=False: self.handle_back())
        top_bar.addWidget(back_button)
        top_bar.addStretch(1)
        container.layout.addLayout(top_bar)
        container.layout.addWidget(create_page_header("系統設定", "可設定攝影機、NAS、本地儲存與員工資料。", show_logo=False))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        camera_card, camera_layout = create_card()
        camera_title = QLabel("攝影機預覽與設定")
        camera_title.setObjectName("sectionTitle")
        camera_layout.addWidget(camera_title)

        camera_hint = QLabel("左側保留 4:3 攝影機預覽畫面，右側集中放攝影機選項，避免操作時誤切設定。")
        camera_hint.setObjectName("settingsHint")
        camera_hint.setWordWrap(True)
        camera_layout.addWidget(camera_hint)

        camera_body = QHBoxLayout()
        camera_body.setContentsMargins(0, 0, 0, 0)
        camera_body.setSpacing(16)

        self.camera_preview = QFrame()
        self.camera_preview.setObjectName("subCard")
        self.camera_preview.setMinimumSize(520, 390)
        self.camera_preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_layout = QVBoxLayout(self.camera_preview)
        preview_layout.setContentsMargins(24, 24, 24, 24)
        preview_layout.setSpacing(10)
        preview_layout.addStretch(1)
        preview_title = QLabel("4:3 攝影機預覽區")
        preview_title.setObjectName("subSectionTitle")
        preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_body = QLabel("正式版會在這裡顯示即時攝影機畫面，供你先確認角度、距離與拍攝範圍。")
        preview_body.setObjectName("settingsHint")
        preview_body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_body.setWordWrap(True)
        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(preview_body)
        preview_layout.addStretch(1)
        camera_body.addWidget(self.camera_preview, 1)

        camera_options = QFrame()
        camera_options.setObjectName("subCard")
        camera_options.setMinimumWidth(320)
        camera_options.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        options_layout = QVBoxLayout(camera_options)
        options_layout.setContentsMargins(20, 20, 20, 20)
        options_layout.setSpacing(14)

        self.camera_combo = NoWheelComboBox()
        self.camera_combo.setMinimumHeight(46)
        self.camera_combo.currentIndexChanged.connect(self.persist_selected_camera)
        options_layout.addWidget(self._build_field_block("預設攝影機", self.camera_combo))

        self.zoom_combo = NoWheelComboBox()
        self.zoom_combo.addItems(["100%", "125%", "150%", "200%"])
        self.zoom_combo.setMinimumHeight(46)
        options_layout.addWidget(self._build_field_block("預覽縮放", self.zoom_combo))

        refresh_camera_button = QPushButton("重新整理相機")
        refresh_camera_button.setObjectName("secondaryButton")
        refresh_camera_button.clicked.connect(lambda _checked=False: self.refresh_camera_options())
        options_layout.addWidget(refresh_camera_button)

        options_note = QLabel("之後可在這裡加入 zoom、鏡像、裁切與曝光等進階設定。")
        options_note.setObjectName("settingsHint")
        options_note.setWordWrap(True)
        options_layout.addWidget(options_note)
        options_layout.addStretch(1)
        camera_body.addWidget(camera_options, 1)
        camera_layout.addLayout(camera_body)

        settings_card, settings_layout = create_card()
        settings_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        settings_title = QLabel("連線與儲存")
        settings_title.setObjectName("sectionTitle")
        settings_layout.addWidget(settings_title)

        self.nas_url_input = QLineEdit()
        self.nas_url_input.setPlaceholderText("例如：http://192.168.1.100:8000")
        settings_layout.addWidget(self._build_field_block("NAS API 位址", self.nas_url_input))

        self.storage_path_input = QLineEdit()
        self.storage_path_input.setPlaceholderText("選擇本地暫存與草稿儲存位置")
        browse_button = QPushButton("選擇資料夾")
        browse_button.setObjectName("secondaryButton")
        browse_button.clicked.connect(lambda _checked=False: self.choose_storage_path())

        storage_widget = QWidget()
        storage_row = QHBoxLayout(storage_widget)
        storage_row.setContentsMargins(0, 0, 0, 0)
        storage_row.setSpacing(12)
        storage_row.addWidget(self.storage_path_input, 1)
        storage_row.addWidget(browse_button)
        settings_layout.addWidget(self._build_field_block("本地儲存路徑", storage_widget))

        save_row = QHBoxLayout()
        save_button = QPushButton("儲存連線設定")
        save_button.clicked.connect(lambda _checked=False: self.save_settings())
        save_row.addWidget(save_button)
        save_row.addStretch(1)
        settings_layout.addLayout(save_row)
        settings_layout.addStretch(1)

        employee_card, employee_layout = create_card()
        employee_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        employee_title = QLabel("員工資料設定")
        employee_title.setObjectName("sectionTitle")
        employee_layout.addWidget(employee_title)

        hint = QLabel("表格可直接編輯。選取一筆後可刪除，完成後按「儲存員工資料」。")
        hint.setObjectName("settingsHint")
        hint.setWordWrap(True)
        employee_layout.addWidget(hint)

        self.employee_file_label = QLabel()
        self.employee_file_label.setObjectName("settingsHint")
        self.employee_file_label.setWordWrap(True)
        employee_layout.addWidget(self.employee_file_label)

        button_grid = QGridLayout()
        button_grid.setHorizontalSpacing(12)
        button_grid.setVerticalSpacing(12)
        button_grid.setColumnStretch(0, 1)
        button_grid.setColumnStretch(1, 1)

        add_row_button = QPushButton("新增一筆")
        add_row_button.setObjectName("secondaryButton")
        add_row_button.clicked.connect(lambda _checked=False: self.add_employee_row())
        delete_row_button = QPushButton("刪除選取")
        delete_row_button.setObjectName("secondaryButton")
        delete_row_button.clicked.connect(lambda _checked=False: self.delete_selected_rows())
        download_button = QPushButton("下載範例檔")
        download_button.setObjectName("secondaryButton")
        download_button.clicked.connect(lambda _checked=False: self.download_sample_file())
        import_button = QPushButton("匯入員工檔")
        import_button.setObjectName("secondaryButton")
        import_button.clicked.connect(lambda _checked=False: self.import_employee_file())
        save_employee_button = QPushButton("儲存員工資料")
        save_employee_button.clicked.connect(lambda _checked=False: self.save_employee_table())

        button_grid.addWidget(add_row_button, 0, 0)
        button_grid.addWidget(delete_row_button, 0, 1)
        button_grid.addWidget(download_button, 1, 0)
        button_grid.addWidget(import_button, 1, 1)
        button_grid.addWidget(save_employee_button, 2, 0, 1, 2)
        employee_layout.addLayout(button_grid)

        self.employee_table = QTableWidget(0, 2)
        self.employee_table.setHorizontalHeaderLabels(["員工編號", "員工名稱"])
        self.employee_table.verticalHeader().setVisible(False)
        self.employee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.employee_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.setItemDelegate(CenteredTableDelegate(self.employee_table))
        self.employee_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.employee_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.employee_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.employee_table.setMinimumHeight(260)
        employee_layout.addWidget(self.employee_table, 1)

        self.employee_count_label = QLabel()
        self.employee_count_label.setObjectName("settingsHint")
        employee_layout.addWidget(self.employee_count_label)

        lower_row = QGridLayout()
        lower_row.setHorizontalSpacing(16)
        lower_row.setVerticalSpacing(16)
        lower_row.setColumnStretch(0, 1)
        lower_row.setColumnStretch(1, 1)
        lower_row.addWidget(settings_card, 0, 0)
        lower_row.addWidget(employee_card, 0, 1)

        scroll_layout.addWidget(camera_card)
        scroll_layout.addLayout(lower_row)
        scroll_layout.addStretch(1)
        self.scroll_area.setWidget(scroll_content)

        container.layout.addWidget(self.scroll_area, 1)
        container.layout.addWidget(build_footer())

    def refresh(self) -> None:
        settings = self.window.settings_service.load()
        self.nas_url_input.setText(settings.nas_url)
        self.storage_path_input.setText(settings.local_storage_path)
        self.refresh_camera_options()
        self.refresh_employee_table()
        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(0))

    def refresh_camera_options(self) -> None:
        cameras = self.window.camera_service.list_cameras()
        selected_camera = self.window.camera_service.get_selected_camera(cameras)
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        if not cameras:
            self.camera_combo.addItem("沒有偵測到相機", "")
            self.camera_combo.setEnabled(False)
        else:
            self.camera_combo.setEnabled(True)
            for camera in cameras:
                self.camera_combo.addItem(camera.name, camera.id)
            selected_index = 0
            if selected_camera is not None:
                for index, camera in enumerate(cameras):
                    if camera.id == selected_camera.id:
                        selected_index = index
                        break
            self.camera_combo.setCurrentIndex(selected_index)
        self.camera_combo.blockSignals(False)

    def persist_selected_camera(self) -> None:
        camera_id = str(self.camera_combo.currentData())
        if camera_id:
            self.window.camera_service.save_selected_camera_id(camera_id)

    def _build_field_block(self, label_text: str, field_widget: QWidget) -> QWidget:
        block = QWidget()
        layout = QVBoxLayout(block)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
        layout.addWidget(field_widget)
        return block

    def handle_back(self) -> None:
        if self.window.settings_return_page == "mode":
            self.window.show_mode()
            return
        self.window.show_login()

    def choose_storage_path(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "選擇本地儲存資料夾", self.storage_path_input.text())
        if directory:
            self.storage_path_input.setText(directory)

    def save_settings(self) -> None:
        settings = AppSettings(
            nas_url=self.nas_url_input.text().strip(),
            local_storage_path=self.storage_path_input.text().strip(),
        )
        self.window.settings_service.save(settings)
        QMessageBox.information(self, "儲存完成", "連線與儲存設定已更新。")

    def add_employee_row(self) -> None:
        row_index = self.employee_table.rowCount()
        self.employee_table.insertRow(row_index)
        employee_id_item = QTableWidgetItem("")
        employee_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        employee_name_item = QTableWidgetItem("")
        employee_name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.employee_table.setItem(row_index, 0, employee_id_item)
        self.employee_table.setItem(row_index, 1, employee_name_item)
        self.employee_table.setCurrentCell(row_index, 0)
        self.employee_table.editItem(self.employee_table.item(row_index, 0))

    def delete_selected_rows(self) -> None:
        rows = sorted({index.row() for index in self.employee_table.selectedIndexes()}, reverse=True)
        if not rows:
            QMessageBox.information(self, "尚未選取", "請先選取要刪除的員工資料。")
            return
        for row in rows:
            self.employee_table.removeRow(row)
        self.employee_count_label.setText(f"目前員工資料筆數：{self.employee_table.rowCount()}")

    def download_sample_file(self) -> None:
        target_path, _ = QFileDialog.getSaveFileName(self, "下載員工範例檔", "packpal-employees-sample.csv", "CSV 檔案 (*.csv)")
        if not target_path:
            return
        self.window.employee_service.export_sample_csv(target_path)
        QMessageBox.information(self, "下載完成", f"員工範例檔已輸出到：\n{target_path}")

    def import_employee_file(self) -> None:
        source_path, _ = QFileDialog.getOpenFileName(self, "匯入員工檔", "", "CSV 檔案 (*.csv)")
        if not source_path:
            return
        try:
            count = self.window.employee_service.import_csv(source_path)
        except ValueError as error:
            QMessageBox.warning(self, "匯入失敗", str(error))
            return
        self.refresh_employee_table()
        QMessageBox.information(self, "匯入完成", f"已匯入 {count} 筆員工資料。")

    def save_employee_table(self) -> None:
        records: list[EmployeeRecord] = []
        for row_index in range(self.employee_table.rowCount()):
            employee_id_item = self.employee_table.item(row_index, 0)
            name_item = self.employee_table.item(row_index, 1)
            employee_id = employee_id_item.text().strip() if employee_id_item else ""
            name = name_item.text().strip() if name_item else ""
            if employee_id and name:
                records.append(EmployeeRecord(employee_id=employee_id, name=name))
        if not records:
            QMessageBox.warning(self, "資料不足", "請至少保留一筆完整的員工編號與員工名稱。")
            return
        count = self.window.employee_service.save_records(records)
        self.refresh_employee_table()
        QMessageBox.information(self, "儲存完成", f"已儲存 {count} 筆員工資料。")

    def refresh_employee_table(self) -> None:
        records = self.window.employee_service.load_records()
        self.employee_table.setRowCount(len(records))
        for row_index, record in enumerate(records):
            employee_id_item = QTableWidgetItem(record.employee_id)
            employee_id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            employee_name_item = QTableWidgetItem(record.name)
            employee_name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.employee_table.setItem(row_index, 0, employee_id_item)
            self.employee_table.setItem(row_index, 1, employee_name_item)
        self.employee_count_label.setText(f"目前員工資料筆數：{len(records)}")
        self.employee_file_label.setText(f"目前員工檔：{self.window.employee_service.employee_file_path()}")


class WorkflowPage(QWidget):
    def __init__(self, window: "AppWindow", *, module_key: str, title: str, prompt: str, subtitle: str, scan_placeholder: str, primary_color: str, hover_color: str, gradient_start: str, gradient_end: str) -> None:
        super().__init__()
        self.window = window
        self.module_key = module_key

        container = ScreenContainer()
        container.layout.setContentsMargins(0, 0, 0, 0)
        container.layout.setSpacing(0)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(container)

        stage = QFrame()
        stage.setObjectName("cameraStage")
        stage_layout = QVBoxLayout(stage)
        stage_layout.setContentsMargins(24, 24, 24, 24)
        stage_layout.setSpacing(0)

        top_overlay = QHBoxLayout()
        top_overlay.setSpacing(12)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 28px; font-weight: 700;")
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("color: white; font-size: 14px; background: rgba(15,23,42,0.45); padding: 8px 12px; border-radius: 12px;")
        top_overlay.addWidget(title_label)
        top_overlay.addStretch(1)
        top_overlay.addWidget(self.camera_label)
        stage_layout.addLayout(top_overlay)

        stage_layout.addStretch(1)

        center_prompt = QLabel(prompt)
        center_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_prompt.setStyleSheet("color: white; font-size: 34px; font-weight: 700;")
        stage_layout.addWidget(center_prompt)

        sub_prompt = QLabel(subtitle)
        sub_prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_prompt.setStyleSheet("color: rgba(255,255,255,0.82); font-size: 16px;")
        stage_layout.addWidget(sub_prompt)

        stage_layout.addStretch(1)

        bottom_overlay = QVBoxLayout()
        bottom_overlay.setSpacing(12)

        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText(scan_placeholder)
        self.scan_input.setMinimumHeight(56)
        self.scan_input.setStyleSheet("font-size: 24px; background: rgba(255,255,255,0.96);")
        bottom_overlay.addWidget(self.scan_input)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)
        back_button = QPushButton("返回模式選擇")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(lambda _checked=False: self.window.show_mode())
        load_button = QPushButton("載入最近草稿")
        load_button.setObjectName("secondaryButton")
        load_button.clicked.connect(lambda _checked=False: self.load_latest_draft())
        save_button = QPushButton("儲存草稿")
        save_button.clicked.connect(lambda _checked=False: self.save_draft())
        self.draft_status_label = QLabel("尚未儲存草稿")
        self.draft_status_label.setStyleSheet("color: white; font-size: 14px;")
        action_row.addWidget(back_button)
        action_row.addWidget(load_button)
        action_row.addWidget(save_button)
        action_row.addStretch(1)
        action_row.addWidget(self.draft_status_label)
        bottom_overlay.addLayout(action_row)
        stage_layout.addLayout(bottom_overlay)

        container.layout.addWidget(stage)
        self.setStyleSheet(app_stylesheet(primary_color, hover_color) + f"QFrame#cameraStage {{ background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {gradient_start}, stop:1 {gradient_end}); }}")

    def refresh(self) -> None:
        self.camera_label.setText(f"相機：{self.window.selected_camera_name()}")
        self.load_latest_draft()

    def save_draft(self) -> None:
        draft_id = self.window.draft_service.save_draft(module_key=self.module_key, payload={"record_no": self.scan_input.text().strip()}, camera_name=self.window.selected_camera_name())
        self.draft_status_label.setText(f"草稿已儲存，編號 #{draft_id}")

    def load_latest_draft(self) -> None:
        draft = self.window.draft_service.latest_draft(self.module_key)
        payload = self.window.draft_service.parse_payload(draft)
        self.scan_input.setText(payload.get("record_no", ""))
        if draft is None:
            self.draft_status_label.setText("目前沒有草稿。")
            return
        self.draft_status_label.setText(f"已載入草稿 #{draft.id}")


class AppWindow(QMainWindow):
    def __init__(self, *, settings_service: SettingsService | None = None, employee_service: EmployeeService | None = None, camera_service: CameraService | None = None, draft_service: DraftService | None = None) -> None:
        super().__init__()
        self.settings_service = settings_service or SettingsService()
        self.employee_service = employee_service or EmployeeService(self.settings_service)
        self.camera_service = camera_service or CameraService()
        self.draft_service = draft_service or DraftService()
        self.current_employee: EmployeeRecord | None = None
        self.settings_return_page = "login"

        self.setWindowTitle(f"{APP_TITLE} - 進入作業")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        apply_window_icon(self)
        self.setStyleSheet(app_stylesheet())

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self)
        self.mode_page = ModeSelectPage(self)
        self.settings_page = SettingsPage(self)
        self.shipment_page = WorkflowPage(self, module_key="shipments", title="出貨作業", prompt="請掃描單號開始錄影", subtitle="目前為骨架版，正式版會在這裡顯示即時攝影機畫面並開始錄影。", scan_placeholder="請掃描或輸入單號", primary_color="#0f766e", hover_color="#0d5f59", gradient_start="#0f172a", gradient_end="#134e4a")
        self.repair_page = WorkflowPage(self, module_key="repairs", title="維修收貨", prompt="請掃描維修單號開始收貨", subtitle="正式版會在這裡顯示相機畫面、設備序號與問題摘要收集流程。", scan_placeholder="請掃描或輸入維修單號", primary_color="#b45309", hover_color="#92400e", gradient_start="#422006", gradient_end="#92400e")
        self.return_page = WorkflowPage(self, module_key="returns", title="退貨收貨", prompt="請掃描退貨單號開始收貨", subtitle="正式版會在這裡顯示相機畫面、退貨原因與外觀檢查流程。", scan_placeholder="請掃描或輸入退貨單號", primary_color="#7c3aed", hover_color="#6d28d9", gradient_start="#2e1065", gradient_end="#6d28d9")

        self.pages = {
            "login": self.login_page,
            "mode": self.mode_page,
            "settings": self.settings_page,
            "shipment": self.shipment_page,
            "repair": self.repair_page,
            "return": self.return_page,
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.show_login()

    def closeEvent(self, event: QCloseEvent) -> None:
        app = QApplication.instance()
        if app is not None:
            app.quit()
        event.accept()

    def show_login(self) -> None:
        self.setWindowTitle(f"{APP_TITLE} - 進入作業")
        self.stack.setCurrentWidget(self.login_page)
        self.login_page.reset()

    def show_mode(self, employee: EmployeeRecord | None = None) -> None:
        if employee is not None:
            self.current_employee = employee
        self.setWindowTitle(f"{APP_TITLE} - 模式選擇")
        self.mode_page.refresh()
        self.stack.setCurrentWidget(self.mode_page)

    def show_settings(self, return_page: str) -> None:
        self.settings_return_page = return_page
        self.setWindowTitle(f"{APP_TITLE} - 系統設定")
        self.settings_page.refresh()
        self.stack.setCurrentWidget(self.settings_page)

    def show_workflow(self, workflow_key: str) -> None:
        page = self.pages[workflow_key]
        titles = {"shipment": "出貨作業", "repair": "維修收貨", "return": "退貨收貨"}
        self.setWindowTitle(f"{APP_TITLE} - {titles[workflow_key]}")
        page.refresh()
        self.stack.setCurrentWidget(page)

    def selected_camera_name(self) -> str:
        return self.mode_page.selected_camera_name()






