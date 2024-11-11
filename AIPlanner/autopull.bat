@echo off

:: Run the commands
echo Checking out to main...
git checkout main

echo Pulling main...
git pull

echo Checking out to beta...
git checkout beta

echo Pulling beta...
git pull

echo Main and Beta branches updated successfully. If you are creating a new branch for a feature, run "git branch branch_name". If you are editing an existing branch, run "git checkout branch_name".

pause