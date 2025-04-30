@echo off
mkdir backup
copy app.py backup\
copy requirements.txt backup\
copy Dockerfile backup\
copy docker-compose.yml backup\
copy .dockerignore backup\
xcopy /E /I templates backup\templates
xcopy /E /I instance backup\instance
echo Backup concluído! 