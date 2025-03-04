# Flashcard App

## Author: Filip Kobus

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Visuals](#visuals)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Classes Overview](#classes-overview)
7. [License](#license)

## Introduction
This project is a web-based Flashcard application that allows users to create, manage, and study flashcards. The app features an interactive board where users can upload images, generate covering boxes, and toggle text visibility. The backend is built with Flask and AWS services.

## Try it out
https://www.filip-kobus.ink/

## Features
- 📌 User authentication
- 🖼️ Upload images (AWS S3)
- 🌐 Deployed with AWS Elastic Beanstalk
- 🛢️ Uses PostgreSQL on AWS RDS
- 🔍 Text detection using Google Cloud Vision for automatic box creation

## Visuals
<p align="center">
  <img src="https://github.com/user-attachments/assets/86ef640a-fe33-4449-bce6-4f33bc55efc7" alt="Dashboard"/>
  <img src="https://github.com/user-attachments/assets/1f4940e5-680d-49df-b0a6-178a7c169080" alt="Flashcards"/>
  <img src="https://github.com/user-attachments/assets/49334897-93e5-463f-becc-6b8eeca9e75c" alt="Flashcard View"/>
</p>

---

## Installation
To install and run this project, follow these steps:

### 1. Clone the Repository
```sh
git clone https://github.com/filip-kobus/flask-flashcards-app.git
```

### 2. Navigate to the Project Directory
```sh
cd flask-flashcards-app
```

### 3. Create and Activate a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Set Up AWS S3 for Image Storage
#### 5.1 Create an AWS S3 Bucket
- Log in to [AWS Console](https://aws.amazon.com/console/).
- Navigate to **S3** and create a new bucket.
- Enable public access (or configure IAM roles if needed).
- Copy the bucket name for later use.

#### 5.2 Configure AWS Credentials
If you haven't configured AWS CLI yet, run:
```sh
aws configure
```
Provide:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `eu-central-1`)
- Output format (default: `json`)

### 6. Set Up a PostgreSQL Database
- Install **PostgreSQL** if it's not already installed.
- Connect database to sql alchemy using utils/config.py file
- Initialize tables
```sh
from flashcardmaker import db, app

with app.app_context():
    db.create_all()
```

### 7. Configure the Application (`config.py`)
Edit the `config.py` file and fill in the required credentials:
```python
DATABASE_URL = "postgresql://flashcards_user:your_secure_password@localhost/flashcards_db"
AWS_S3_BUCKET = "your-s3-bucket-name"
AWS_ACCESS_KEY = "your-access-key"
AWS_SECRET_KEY = "your-secret-key"
```

### 8. Set Up Google Vision API Credentials
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project and enable **Google Vision API**.
- Generate a **Service Account Key** (`.json` file).
- Download it and save it inside the project as `vision-api-keys.json`.

### 9. Run the Application
```sh
python application.py
```

### 10. (Optional) Deploy to AWS Elastic Beanstalk
```sh
eb init
eb create flashcard-app-env
```

## Usage
1. **Sign in or register.**
2. **Create a new flashcard directory.**
3. **Upload images and generate interactive text overlays.**
4. **Enjoy your studying**

## Classes Overview
- `routes.py`: Handles routes related to flashcard management.
- `forms.py`: Manages user authentication and access control.
- `s3_manager.py`: Handles file uploads and interactions with AWS S3.
- `models.py`: Defines database models using SQLAlchemy.
- `config.py`: Stores environment variables and AWS credentials.
- `__init__.py`: Initializes the Flask application and database.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

