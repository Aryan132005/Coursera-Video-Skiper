@echo off
if "%~1"=="" (
    echo [Usage] Kripya course ka slug provide karein.
    echo Example: run.bat course-slug
    echo Example ^(with AI quiz solver^): run.bat course-slug --llm
    exit /b 1
)
"%~dp0venv\Scripts\skipera.exe" %*
