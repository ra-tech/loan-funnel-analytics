USE loan_funnel_analytics;

-- =========================================================
-- SAMPLE USERS
-- =========================================================

INSERT INTO users
(signup_date, city, age, acquisition_channel)
VALUES
('2026-01-05', 'Delhi', 24, 'Google Ads'),
('2026-01-07', 'Mumbai', 31, 'Referral'),
('2026-01-08', 'Bengaluru', 27, 'Instagram'),
('2026-01-10', 'Delhi', 35, 'Organic'),
('2026-01-12', 'Gurugram', 29, 'Referral');


-- =========================================================
-- SAMPLE LOAN APPLICATIONS
-- =========================================================

INSERT INTO loan_applications
(user_id, application_date, loan_amount, tenure_months, status)
VALUES
(1, '2026-01-05', 300000, 36, 'Disbursed'),
(2, '2026-01-08', 500000, 48, 'Approved'),
(3, '2026-01-09', 150000, 24, 'Rejected'),
(4, '2026-01-11', 400000, 36, 'Disbursed'),
(5, '2026-01-13', 250000, 24, 'KYC Pending');


-- =========================================================
-- SAMPLE APPLICATION EVENTS
-- =========================================================

INSERT INTO application_events
(application_id, event_name, event_time)
VALUES

-- Application 1: Successfully disbursed
(1, 'Application Started', '2026-01-05 10:00:00'),
(1, 'Details Completed', '2026-01-05 10:08:00'),
(1, 'KYC Completed', '2026-01-05 10:20:00'),
(1, 'Offer Viewed', '2026-01-05 12:00:00'),
(1, 'Offer Accepted', '2026-01-05 12:10:00'),
(1, 'Loan Disbursed', '2026-01-06 09:00:00'),

-- Application 2: Approved but not yet disbursed
(2, 'Application Started', '2026-01-08 11:00:00'),
(2, 'Details Completed', '2026-01-08 11:07:00'),
(2, 'KYC Completed', '2026-01-08 11:20:00'),
(2, 'Offer Viewed', '2026-01-08 15:00:00'),

-- Application 3: Rejected after KYC
(3, 'Application Started', '2026-01-09 14:00:00'),
(3, 'Details Completed', '2026-01-09 14:05:00'),
(3, 'KYC Completed', '2026-01-09 14:15:00'),

-- Application 4: Successfully disbursed
(4, 'Application Started', '2026-01-11 09:30:00'),
(4, 'Details Completed', '2026-01-11 09:40:00'),
(4, 'KYC Completed', '2026-01-11 10:00:00'),
(4, 'Offer Viewed', '2026-01-11 12:30:00'),
(4, 'Offer Accepted', '2026-01-11 12:45:00'),
(4, 'Loan Disbursed', '2026-01-12 10:00:00'),

-- Application 5: Customer drops before KYC completion
(5, 'Application Started', '2026-01-13 16:00:00'),
(5, 'Details Completed', '2026-01-13 16:12:00');