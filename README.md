# Loan Application Funnel Analytics

A MySQL-based product analytics project exploring customer behaviour across a simulated digital lending journey.

The project models users, loan applications, and application events to analyse how customers move through a loan application funnel and where they drop off.

## Project Objective

The goal of this project is to use SQL to answer product and business questions such as:

- What percentage of applications are successfully disbursed?
- At which stage do customers drop out most frequently?
- Which acquisition channels generate the highest conversion rates?
- How does loan performance vary across cities and customer segments?
- How long does a customer typically take to move from application to disbursement?

## Database Structure

The database currently contains three relational tables:

### `users`
Stores customer-level information including:
- signup date
- city
- age
- acquisition channel

### `loan_applications`
Stores loan application information including:
- customer
- application date
- requested loan amount
- tenure
- application status

### `application_events`
Stores events representing the customer's journey through the application funnel.

Example events include:

Application Started → Details Completed → KYC Completed → Offer Viewed → Offer Accepted → Loan Disbursed

## Tech Stack

- MySQL
- SQL
- Python *(for synthetic data generation)*

## Repository Structure

```text
loan-funnel-analytics/
│
├── README.md
├── sql/
│   └── schema.sql
├── data/
└── scripts/