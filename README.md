# Loan Application Funnel Analytics

A MySQL-based product analytics project that models and analyses a simulated digital lending journey.

The project uses a relational database containing users, loan applications and application events to study customer conversion, funnel drop-offs and acquisition-channel performance.

## Project Objective

The goal of this project is to use SQL and product analytics concepts to answer business questions such as:

- What percentage of loan applications are successfully disbursed?
- At which stage do customers drop out most frequently?
- Which acquisition channels generate the highest conversion rates?
- How do application outcomes vary across customer segments and cities?
- Does requested loan amount affect approval probability?
- How long does a customer typically take to move from application to disbursement?

## Database Design

The project uses three relational tables.

### `users`

Stores customer-level information:

- `user_id`
- `signup_date`
- `city`
- `age`
- `acquisition_channel`

### `loan_applications`

Stores loan application information:

- `application_id`
- `user_id`
- `application_date`
- `loan_amount`
- `tenure_months`
- `status`

Each application is linked to a user through a foreign key.

### `application_events`

Stores the customer's progress through the loan application funnel:

- `event_id`
- `application_id`
- `event_name`
- `event_time`

Each event is linked to a loan application through a foreign key.

A typical customer journey may look like:

```text
Application Started
        ↓
Details Completed
        ↓
KYC Completed
        ↓
Offer Viewed
        ↓
Offer Accepted
        ↓
Loan Disbursed