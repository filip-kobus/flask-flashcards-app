# Flashcard App

## Authors: Filip Kobus

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Visuals](#visuals)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Classes Overview](#classes-overview)
8. [Documentation](#documentation)
9. [License](#license)

## Introduction
This project is a web-based Flashcard application that allows users to create, manage, and study flashcards. The app features an interactive board where users can upload images, generate covering boxes, and toggle text visibility. The backend is built with Flask and AWS services.

## Features
- 📌 User authentication
- 🖼️ Upload images (AWS S3)
- 🌐 Deployed with AWS Elastic Beanstalk
- 🛢️ Uses PostgreSQL on AWS RDS
- 🔍 Text detection using Google Cloud Vision for automatic box creation

## Visuals
<p align="center">
  <img src="./static/gallery/dashboard.png" alt="Dashboard" width="45%"/>
  <img src="./static/gallery/flashcards_view.png" alt="Flashcard View" width="45%"/>
</p>

## Installation
To install and run this project, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   ```
   
2. **Navigate to the project directory:**
   ```sh
   cd flashcard-app
   ```
   
3. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   
5. **Set up environment variables:**
   ```sh
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```
   
6. **Run the application:**
   ```sh
   flask run
   ```
   
Alternatively, deploy the application using AWS Elastic Beanstalk:
   ```sh
   eb init
   eb create flashcard-app-env
   ```

## Usage
1. **Sign in or register using AWS Cognito authentication.**
2. **Create a new flashcard directory.**
3. **Upload images and add interactive text overlays.**
4. **Use real-time collaboration features to edit flashcards with other users.**
5. **Save and export flashcards for studying.**

## Project Structure
```plaintext
flashcard-app/
├── static/
│   ├── gallery/
│   │   ├── dashboard.png
│   │   ├── flashcards_view.png
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── flashcards.html
│   ├── admin.html
├── app/
│   ├── routes/
│   │   ├── flashcards.py
│   │   ├── users.py
│   ├── models.py
│   ├── s3_manager.py
│   ├── config.py
│   ├── __init__.py
├── Dokumentacja/
│   ├── Documentation.pdf
│   └── API_Reference.md
├── requirements.txt
├── README.md
└── LICENSE
```

## Classes Overview
- `flashcards.py`: Handles routes related to flashcard management.
- `users.py`: Manages user authentication and access control.
- `s3_manager.py`: Handles file uploads and interactions with AWS S3.
- `models.py`: Defines database models using SQLAlchemy.
- `config.py`: Stores environment variables and AWS credentials.
- `__init__.py`: Initializes the Flask application and database.

## Documentation
For detailed API documentation and project usage, refer to the documentation located in the `Dokumentacja` directory.

📄 [Documentation.pdf](./Dokumentacja/Documentation.pdf)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

