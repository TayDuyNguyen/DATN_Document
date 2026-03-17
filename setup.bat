@echo off
echo ========================================
echo  Setup venv cho crawl_places.py
echo ========================================

:: Tạo virtual environment
python -m venv venv
if errorlevel 1 (
    echo [LOI] Khong tao duoc venv. Kiem tra Python da cai chua.
    pause
    exit /b 1
)

echo [OK] Da tao venv

:: Kích hoạt venv và cài thư viện
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo  Setup xong! Chay lenh sau de crawl:
echo.
echo  venv\Scripts\activate
echo  python crawl_places.py --key YOUR_API_KEY
echo ========================================
pause
