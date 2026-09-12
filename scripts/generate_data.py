import csv
import random
from datetime import date, datetime, timedelta

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

random.seed(42)

NUM_USERS = 5000
NUM_APPLICATIONS = 7000

START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 8, 31)

CITIES = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Gurugram",
    "Pune",
    "Hyderabad",
    "Chennai",
    "Jaipur"
]

CHANNELS = [
    "Google Ads",
    "Instagram",
    "Organic",
    "Referral"
]

CHANNEL_WEIGHTS = [
    0.30,
    0.25,
    0.25,
    0.20
]

LOAN_AMOUNTS = [
    50000,
    100000,
    150000,
    200000,
    250000,
    300000,
    400000,
    500000,
    750000,
    1000000
]

TENURES = [12, 24, 36, 48, 60]


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def random_date(start, end):
    """
    Returns a random date between start and end.
    """

    number_of_days = (end - start).days

    return start + timedelta(
        days=random.randint(0, number_of_days)
    )


def add_minutes(current_time, minimum, maximum):
    """
    Adds a random number of minutes to a datetime.
    """

    return current_time + timedelta(
        minutes=random.randint(minimum, maximum)
    )


def add_hours(current_time, minimum, maximum):
    """
    Adds a random number of hours to a datetime.
    """

    return current_time + timedelta(
        hours=random.randint(minimum, maximum)
    )


# ---------------------------------------------------------
# GENERATE USERS
# ---------------------------------------------------------

users = []

for user_id in range(1, NUM_USERS + 1):

    signup_date = random_date(
        START_DATE,
        date(2026, 7, 31)
    )

    city = random.choice(CITIES)

    age = random.randint(21, 55)

    acquisition_channel = random.choices(
        CHANNELS,
        weights=CHANNEL_WEIGHTS,
        k=1
    )[0]

    users.append({
        "user_id": user_id,
        "signup_date": signup_date,
        "city": city,
        "age": age,
        "acquisition_channel": acquisition_channel
    })


# ---------------------------------------------------------
# GENERATE LOAN APPLICATIONS
# ---------------------------------------------------------

applications = []

# Every user receives at least one application
application_user_ids = list(range(1, NUM_USERS + 1))

# Add another 2,000 applications from existing users
while len(application_user_ids) < NUM_APPLICATIONS:
    application_user_ids.append(
        random.randint(1, NUM_USERS)
    )

random.shuffle(application_user_ids)

users_by_id = {
    user["user_id"]: user
    for user in users
}


# ---------------------------------------------------------
# FUNNEL SETTINGS
# ---------------------------------------------------------

# These probabilities deliberately make channels behave
# differently so our SQL analysis produces meaningful results.

DETAILS_PROBABILITY = {
    "Referral": 0.94,
    "Organic": 0.91,
    "Google Ads": 0.87,
    "Instagram": 0.82
}

KYC_PROBABILITY = {
    "Referral": 0.90,
    "Organic": 0.86,
    "Google Ads": 0.80,
    "Instagram": 0.74
}

APPROVAL_PROBABILITY = {
    "Referral": 0.76,
    "Organic": 0.70,
    "Google Ads": 0.63,
    "Instagram": 0.57
}

OFFER_ACCEPTANCE_PROBABILITY = {
    "Referral": 0.86,
    "Organic": 0.81,
    "Google Ads": 0.74,
    "Instagram": 0.67
}

DISBURSEMENT_PROBABILITY = {
    "Referral": 0.94,
    "Organic": 0.92,
    "Google Ads": 0.89,
    "Instagram": 0.86
}


# ---------------------------------------------------------
# GENERATE APPLICATIONS AND EVENTS
# ---------------------------------------------------------

events = []

event_id = 1

for application_id, user_id in enumerate(
    application_user_ids,
    start=1
):

    user = users_by_id[user_id]

    # Application happens between signup and 45 days later
    application_date = (
        user["signup_date"]
        + timedelta(days=random.randint(0, 45))
    )

    if application_date > END_DATE:
        application_date = END_DATE

    loan_amount = random.choice(LOAN_AMOUNTS)

    tenure_months = random.choice(TENURES)

    channel = user["acquisition_channel"]


    # -----------------------------------------------------
    # EVENT 1: APPLICATION STARTED
    # -----------------------------------------------------

    event_time = datetime.combine(
        application_date,
        datetime.min.time()
    )

    event_time += timedelta(
        hours=random.randint(8, 20),
        minutes=random.randint(0, 59)
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "Application Started",
        "event_time": event_time
    })

    event_id += 1


    # -----------------------------------------------------
    # EVENT 2: DETAILS COMPLETED
    # -----------------------------------------------------

    if random.random() > DETAILS_PROBABILITY[channel]:

        status = "Incomplete"

        applications.append({
            "application_id": application_id,
            "user_id": user_id,
            "application_date": application_date,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "status": status
        })

        continue


    event_time = add_minutes(
        event_time,
        3,
        20
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "Details Completed",
        "event_time": event_time
    })

    event_id += 1


    # -----------------------------------------------------
    # EVENT 3: KYC COMPLETED
    # -----------------------------------------------------

    if random.random() > KYC_PROBABILITY[channel]:

        status = "KYC Pending"

        applications.append({
            "application_id": application_id,
            "user_id": user_id,
            "application_date": application_date,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "status": status
        })

        continue


    event_time = add_minutes(
        event_time,
        5,
        40
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "KYC Completed",
        "event_time": event_time
    })

    event_id += 1


    # -----------------------------------------------------
    # APPROVAL DECISION
    # -----------------------------------------------------

    approval_probability = (
        APPROVAL_PROBABILITY[channel]
    )

    # Larger loans are slightly harder to approve
    if loan_amount >= 750000:
        approval_probability -= 0.15

    elif loan_amount >= 500000:
        approval_probability -= 0.08


    if random.random() > approval_probability:

        status = "Rejected"

        applications.append({
            "application_id": application_id,
            "user_id": user_id,
            "application_date": application_date,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "status": status
        })

        continue


    # -----------------------------------------------------
    # EVENT 4: OFFER VIEWED
    # -----------------------------------------------------

    event_time = add_hours(
        event_time,
        1,
        24
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "Offer Viewed",
        "event_time": event_time
    })

    event_id += 1


    # -----------------------------------------------------
    # EVENT 5: OFFER ACCEPTED
    # -----------------------------------------------------

    if random.random() > OFFER_ACCEPTANCE_PROBABILITY[channel]:

        status = "Approved"

        applications.append({
            "application_id": application_id,
            "user_id": user_id,
            "application_date": application_date,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "status": status
        })

        continue


    event_time = add_minutes(
        event_time,
        5,
        120
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "Offer Accepted",
        "event_time": event_time
    })

    event_id += 1


    # -----------------------------------------------------
    # EVENT 6: LOAN DISBURSED
    # -----------------------------------------------------

    if random.random() > DISBURSEMENT_PROBABILITY[channel]:

        status = "Approved"

        applications.append({
            "application_id": application_id,
            "user_id": user_id,
            "application_date": application_date,
            "loan_amount": loan_amount,
            "tenure_months": tenure_months,
            "status": status
        })

        continue


    event_time = add_hours(
        event_time,
        2,
        48
    )

    events.append({
        "event_id": event_id,
        "application_id": application_id,
        "event_name": "Loan Disbursed",
        "event_time": event_time
    })

    event_id += 1

    status = "Disbursed"

    applications.append({
        "application_id": application_id,
        "user_id": user_id,
        "application_date": application_date,
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "status": status
    })


# ---------------------------------------------------------
# WRITE USERS CSV
# ---------------------------------------------------------

with open(
    "data/users.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "user_id",
            "signup_date",
            "city",
            "age",
            "acquisition_channel"
        ]
    )

    writer.writeheader()
    writer.writerows(users)


# ---------------------------------------------------------
# WRITE APPLICATIONS CSV
# ---------------------------------------------------------

with open(
    "data/loan_applications.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "application_id",
            "user_id",
            "application_date",
            "loan_amount",
            "tenure_months",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(applications)


# ---------------------------------------------------------
# WRITE EVENTS CSV
# ---------------------------------------------------------

with open(
    "data/application_events.csv",
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "event_id",
            "application_id",
            "event_name",
            "event_time"
        ]
    )

    writer.writeheader()
    writer.writerows(events)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print("Synthetic data generated successfully.")
print(f"Users: {len(users)}")
print(f"Loan applications: {len(applications)}")
print(f"Application events: {len(events)}")