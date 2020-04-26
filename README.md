# Description

SMS Twilio app to get earthquake notifications for your area.

## How it works?

### 1. TXT your zipcode to Twilio Number
### 2. Get latest earthquake info
### 3. For another area sent another zipcode to get new update

# App Usage

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


