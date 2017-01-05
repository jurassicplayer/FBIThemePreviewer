for %%f in (*.py) do (
    set script_name=%%~nf
    goto build_exe
)
:build_exe
del /Q %script_name%.exe
start /wait pyinstaller --onefile --icon=favicon.ico %script_name%.py
rmdir /S /Q build
del /Q %script_name%.spec
move /-y dist\%script_name%.exe .\
rmdir /S /Q dist