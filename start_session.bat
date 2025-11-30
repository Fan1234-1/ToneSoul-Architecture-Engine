@echo off
echo ==========================================
echo       ToneSoul v2.0 - Session Start
echo ==========================================
echo.
echo [1/2] Loading Memory Context...
python memory/loader.py
echo.
echo [2/2] System Ready.
echo.
echo You can now start interacting with the agent.
echo To run the internal meeting simulation, type:
echo python simulations/internal_meeting.py
echo.
pause
