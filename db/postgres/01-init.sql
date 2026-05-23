CREATE TABLE hospitals (
    hospital_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    org_type VARCHAR(20) NOT NULL,
    state CHAR(2) NOT NULL
);

CREATE TABLE patients (
    patient_id INTEGER PRIMARY KEY,
    hospital_id INTEGER NOT NULL REFERENCES hospitals(hospital_id),
    age INTEGER NOT NULL,
    insurance_type VARCHAR(20) NOT NULL
);

CREATE TABLE encounters (
    encounter_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    visit_date DATE NOT NULL,
    department VARCHAR(30) NOT NULL
);

CREATE TABLE device_orders (
    order_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id),
    device_name VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL
);

\i /docker-entrypoint-initdb.d/seed.sql

CREATE USER learner_ro WITH PASSWORD 'learner';
GRANT CONNECT ON DATABASE healthcare TO learner_ro;
GRANT USAGE ON SCHEMA public TO learner_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO learner_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO learner_ro;
