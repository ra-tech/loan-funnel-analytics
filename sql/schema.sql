CREATE DATABASE loan_funnel_analytics;

USE loan_funnel_analytics;


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    signup_date DATE NOT NULL,
    city VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    acquisition_channel VARCHAR(50) NOT NULL
);


CREATE TABLE loan_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    application_date DATE NOT NULL,
    loan_amount DECIMAL(12,2) NOT NULL,
    tenure_months INT NOT NULL,
    status VARCHAR(30) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE application_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    event_name VARCHAR(50) NOT NULL,
    event_time DATETIME NOT NULL,

    FOREIGN KEY (application_id) REFERENCES loan_applications(application_id)
);