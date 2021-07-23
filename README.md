# Argyle Upwork Scanner

This is a development task for Argyle Scan Engineer

## Setup

### **Running as local environment API**

#### **Login variables**

Rename _.login-sample.json_ to _.login.json_, then fill all necessary(login, password) values:

```json
{
    "login": <username>,
    "password": <password>,
    "secret_answer":,
    "auth_secret_key":
}
```

#### **Installing dependencies**

Using pip:

```bash
pip install requirements.txt
```

or, using poetry to manage dependencies:

```bash
pip install poetry
poetry install --no-interaction
```

#### **Running locally**

```bash
gunicorn --reload --log-level debug --timeout 100 wsgi:app
```

## Usage

By the way, it's not necessary to setup an API. It's possible to generate a json output for those scraping methods:

1. **profile**: `Scraping().get_profile_content()`. Following profile object described here [https://argyle.com/docs/api-reference/profiles](https://argyle.com/docs/api-reference/profiles)
2. **works**: `Scraping().get_portal_content()`
3. **full_profile**: `Scraping().get_full_profile_content()`. Extra method that show more profile details.

All methods will save a individual json file at **ouput** path.

## Models

**Work**

```
title: str
url: str
description: str
tags: List[str]
location: str
client_spendings: str
payment_status: str
rating: str
job_type: str
tier: str
date: datetime
```

**Profile**

```
id: int
account: str
employer: str
created_at: datetime
updated_at: Optional[datetime]
first_name: str
last_name: str
full_name: str
email: str
phone_number: int
birth_date: Optional[datetime]
picture_url: str
address: Address
ssn: Optional[int]
marital_status: Optional[str]
gender: Optional[str]
metadata: dict = {}
```

ps.: **full_profile** model is to bigger

## Docker [improving]

Build a container from this scraping application:

```bash
docker build -t upwork-scanner -f Dockerfile .
```

Run API:

```bash
docker run -d -p 8000:8000 upwork-scanner
```

## Tests [coding]

Run `pytest` to follow up its application unit test coverage.

## About Me

### **Luís Guilherme Medeiros de Farias**

**Software Engineer.**

**Paraná, Brazil**

Email: luisgmfarias@gmail.com

Portfolio: luisgmfarias.github.io
