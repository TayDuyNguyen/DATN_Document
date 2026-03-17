@echo off
echo ========================================
echo  Xoa venv
echo ========================================

if exist venv (
    rmdir /s /q venv
    echo [OK] Da xoa thu muc venv
) else (
    echo [INFO] Khong tim thay venv, bo qua
)

echo Xong!
pause
