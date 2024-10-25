@echo off

:: Delete the files alembic.ini and reflex.db if they exist
if exist alembic.ini (
    del /f /q alembic.ini
    echo Deleted alembic.ini
) else (
    echo alembic.ini not found
)

if exist reflex.db (
    del /f /q reflex.db
    echo Deleted reflex.db
) else (
    echo reflex.db not found
)

:: Delete the folder alembic if it exists
if exist alembic (
    rmdir /s /q alembic
    echo Deleted alembic folder
) else (
    echo alembic folder not found
)

:: Run the commands
echo Initializing database...
reflex db init

echo Making migrations...
reflex db makemigrations

echo Running migrations...
reflex db migrate

echo All tasks completed.
pause