SHOW DATABASES;
CREATE DATABASE DbName;
USE DbName;
SHOW TABLES;
CREATE TABLE TableName (
	id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    birthDate DATE,
    eventTime TIME,
    createdAt DATETIME,
    isActive TINYINT(1),
    price DECIMAL(10,2),
    status ENUM('active', 'inactive'),
    personID INT FOREIGN KEY REFERENCES Persons(personID)
);
CREATE OR REPLACE VIEW ActiveUsers AS SELECT id, name FROM TableName WHERE isActive = 1;

DROP TABLE IF EXISTS TableName;
RENAME TABLE OldTableName TO NewTableName;
ALTER TABLE TableName ADD COLUMN newColumn INT AFTER name;
ALTER TABLE TableName MODIFY COLUMN name VARCHAR(100);
ALTER TABLE TableName CHANGE COLUMN oldColumnName newColumnName INT;
ALTER TABLE TableName DROP COLUMN IF EXISTS columnToBeDropped;
CREATE INDEX idxName ON TableName(nameCol);

INSERT INTO TableName (name, desc) VALUES ('John', 'description');
UPDATE TableName SET isActive = 1, desc = 'desc' WHERE id = 1;
DELETE FROM TableName WHERE id = 1;
SELECT * FROM TableName WHERE isActive = 1;
SELECT * FROM ActiveUsers ORDER BY createdAt DESC;
SELECT * FROM TableName LIMIT 10;
SELECT DISTINCT status FROM TableName; -- if only 2 statuses, only 2 statuses return
SELECT tn.id, ot.someColumn FROM TableName tn
	INNER JOIN OtherTable ot ON tn.id = ot.otherId;
SELECT * FROM TableName WHERE name LIKE 'J%'; -- Justin, James, etc.
SELECT * FROM TableName WHERE birthDate BETWEEN '1990-01-01' AND '2000-12-31';
SELECT * FROM TableName WHERE columnName = (SELECT MAX(columnName) FROM TableName);
SELECT * FROM Employees WHERE departmentId IN (SELECT departmentId FROM Departments WHERE departmentName IN ('IT', 'Finance', 'Marketing'));


SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM TableName WHERE columnName = 'some_value';
SELECT status, COUNT(*) as statusCount
	FROM TableName GROUP BY status; -- active 2, inactive 3
SELECT status, COUNT(*) as statusCount
	FROM TableName GROUP BY status HAVING statusCount > 5;
SELECT department, SUM(salary) as totalSalary
	FROM employees GROUP BY department HAVING totalSalary > 50000;

CREATE TRIGGER triggerName BEFORE INSERT ON TableName FOR EACH ROW SET NEW.createdAt = NOW();
START TRANSACTION;
-- Your SQL queries here
COMMIT;
SELECT name AS employee_name, birthDate AS birth_date FROM TableName;
