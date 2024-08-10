-- settings.sql
CREATE DATABASE quizmate;
CREATE USER quizmate_user WITH PASSWORD 'quizmate';
GRANT ALL PRIVILEGES ON DATABASE quizmate TO quizmate_user;