$ErrorActionPreference = "Stop"

python -m pip install -r requirements.txt
python -m pip install -r build-requirements.txt
python -m PyInstaller --noconfirm packpal-windows.spec