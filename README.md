# Description

SMS Twilio app to get earthquake notifications for your area straight to your phone.

# Usage

1. Clone the repo
2. `cd` into the repo
3. Run following commands:
    - `pipenv install`
    - `pipenv shell`
    - `python run.py`


# Routes

| Method | Endpoint | Access Control | Description                                              |
| ------ | -------- | -------------- | -------------------------------------------------------- |
| POST   | `/sms`   | all users      | Returns the earthquake information for your area. |
