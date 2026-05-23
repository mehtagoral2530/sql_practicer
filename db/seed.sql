-- Shared seed data (logical rows identical on both engines)

INSERT INTO hospitals (hospital_id, name, org_type, state) VALUES
(1, 'Riverside Medical Center', 'for_profit', 'CA'),
(2, 'Lakeview Community Hospital', 'non_profit', 'CA'),
(3, 'Summit Health Partners', 'for_profit', 'TX'),
(4, 'Harbor Care Hospital', 'non_profit', 'NY'),
(5, 'Prairie Regional Medical', 'for_profit', 'IL');

INSERT INTO patients (patient_id, hospital_id, age, insurance_type) VALUES
(101, 1, 34, 'commercial'),
(102, 1, 67, 'medicare'),
(103, 2, 45, 'medicaid'),
(104, 2, 29, 'commercial'),
(105, 3, 52, 'medicare'),
(106, 3, 38, 'commercial'),
(107, 4, 71, 'medicare'),
(108, 4, 41, 'commercial'),
(109, 5, 58, 'medicare'),
(110, 5, 33, 'commercial'),
(111, 1, 49, 'commercial'),
(112, 2, 62, 'medicare');

INSERT INTO encounters (encounter_id, patient_id, visit_date, department) VALUES
(1001, 101, '2024-01-15', 'emergency'),
(1002, 101, '2024-02-20', 'cardiology'),
(1003, 102, '2024-01-22', 'orthopedics'),
(1004, 103, '2024-03-01', 'emergency'),
(1005, 104, '2024-02-10', 'primary_care'),
(1006, 105, '2024-01-30', 'cardiology'),
(1007, 106, '2024-03-15', 'emergency'),
(1008, 107, '2024-02-05', 'oncology'),
(1009, 108, '2024-03-20', 'primary_care'),
(1010, 109, '2024-01-18', 'orthopedics'),
(1011, 110, '2024-02-28', 'emergency'),
(1012, 111, '2024-03-10', 'cardiology'),
(1013, 112, '2024-01-25', 'primary_care'),
(1014, 103, '2024-04-01', 'cardiology'),
(1015, 105, '2024-04-05', 'emergency');

INSERT INTO device_orders (order_id, patient_id, device_name, unit_cost, order_date) VALUES
(2001, 101, 'Insulin Pump', 4500.00, '2024-01-20'),
(2002, 102, 'Knee Implant', 8200.00, '2024-02-01'),
(2003, 103, 'Pacemaker', 12000.00, '2024-03-05'),
(2004, 105, 'Insulin Pump', 4500.00, '2024-01-25'),
(2005, 107, 'Hip Implant', 9500.00, '2024-02-15'),
(2006, 109, 'Knee Implant', 8200.00, '2024-01-30'),
(2007, 111, 'Pacemaker', 12000.00, '2024-03-12'),
(2008, 104, 'Glucose Monitor', 350.00, '2024-02-20'),
(2009, 106, 'Glucose Monitor', 350.00, '2024-03-18'),
(2010, 108, 'Insulin Pump', 4500.00, '2024-03-22'),
(2011, 110, 'Knee Implant', 8200.00, '2024-02-28'),
(2012, 112, 'Pacemaker', 12000.00, '2024-01-28');
