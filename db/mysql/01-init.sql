CREATE TABLE hospitals (
    hospital_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    org_type VARCHAR(20) NOT NULL,
    state CHAR(2) NOT NULL
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    hospital_id INT NOT NULL,
    age INT NOT NULL,
    insurance_type VARCHAR(20) NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

CREATE TABLE encounters (
    encounter_id INT PRIMARY KEY,
    patient_id INT NOT NULL,
    visit_date DATE NOT NULL,
    department VARCHAR(30) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE device_orders (
    order_id INT PRIMARY KEY,
    patient_id INT NOT NULL,
    device_name VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

SOURCE /docker-entrypoint-initdb.d/seed.sql;

CREATE USER IF NOT EXISTS 'learner_ro'@'%' IDENTIFIED BY 'learner';
GRANT SELECT ON healthcare.* TO 'learner_ro'@'%';
FLUSH PRIVILEGES;
