#!/bin/bash

# Delete the files alembic.ini and reflex.db if they exist
if [ -f "alembic.ini" ]; then
    rm alembic.ini
    echo "Deleted alembic.ini"
else
    echo "alembic.ini not found"
fi

if [ -f "reflex.db" ]; then
    rm reflex.db
    echo "Deleted reflex.db"
else
    echo "reflex.db not found"
fi

# Delete the folder alembic if it exists
if [ -d "alembic" ]; then
    rm -r alembic
    echo "Deleted alembic folder"
else
    echo "alembic folder not found"
fi

# Run the commands
echo "Initializing database..."
reflex db init

echo "Making migrations..."
reflex db makemigrations

echo "Running migrations..."
reflex db migrate

echo "All tasks completed."
