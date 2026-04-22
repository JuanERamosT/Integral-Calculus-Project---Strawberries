@echo off
echo ============================================
echo  Configuracion del Proyecto - Fresas
echo  Calculo Integral I - Unillanos
echo ============================================
echo.

echo [1/3] Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate

echo [2/3] Instalando dependencias...
pip install -r requirements.txt

echo [3/3] Listo!
echo.
echo Para ejecutar la app:
echo   cd app
echo   python app.py
echo.
echo Luego abre: http://localhost:5000
pause
