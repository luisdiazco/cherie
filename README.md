
# Cherie

## Description
Cherie is a reselling store web application developed as a Zappos take-home project.
This project focuses on user authentication (using static user/password for basic authentication),
Bootstrap CSS styling, and pagination for lists with more than 10 rows.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Features
- User authentication with basic static credentials.
- Bootstrap CSS styling for an enhanced user interface.
- Pagination for lists with more than 10 rows.

## Installation
1. Clone this repository to your local machine using Git:
   ```bash
   git clone <repository_url>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Configure your environment variables.

2. Run the Flask application:
   ```bash
   python run.py
   ```

## Configuration
1. Create a .env file in the root directory.

2. Add the following environment variables to the .env file:
   ```bash
   AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
   AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
   AWS_DEFAULT_REGION="<AWS_DEFAULT_REGION>"
   SECRET_KEY="<SECRET_KEY>"
   ```


