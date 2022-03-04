@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
set "VIRTUAL_ENV=D:\work\snaResearchTrends"

if defined _OLD_VIRTUAL_PYTHONHOME (
    set "PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%"
)

if defined PYTHONHOME (
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
    set PYTHONHOME=
)

if defined _OLD_VIRTUAL_PATH (
    set "PATH=%_OLD_VIRTUAL_PATH%"
) else (
    set "_OLD_VIRTUAL_PATH=%PATH%"
)

set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set INPUT=EdgeTest.txt

python %VIRTUAL_ENV%\myNetworkAnalysis.py %INPUT%

:END
