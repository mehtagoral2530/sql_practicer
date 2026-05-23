CREATE USER IF NOT EXISTS 'learner_ro'@'%' IDENTIFIED BY 'learner';
GRANT SELECT ON healthcare.* TO 'learner_ro'@'%';
FLUSH PRIVILEGES;
