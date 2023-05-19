
# Vitl Bot

This repository contains code for a chatbot web application using Flask, SQLite, OpenAI's API, and the Langchain. This chatbot conducts a conversation with a user, focused on nutrition and vitamin intake. The application records user responses and identifies discrepancies in their answers based on their conversation with the bot.

## Table of Contents

- [Installation](#installation) 
- [Project Structure](#project-structure) 
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with the application, follow these steps:

1.  Clone this repository to your local machine.

`git clone <this repository URL>` 

2.  Navigate to the project directory.

    ```cd Vitl_bot``` 

3.  Install the required Python packages. It's recommended to use a virtual environment.


```pip install -r requirements.txt``` 

4.  Run the Flask application.

    ```python app.py``` 

5.  Open your browser and go to ```http://localhost:5000```

## Usage

This application includes a chatbot that converses with the user about their nutrition and vitamin intake. It records the conversation, stores it in a SQLite database, and identifies any discrepancies in the user's responses based on their conversation.

To start a chat:

1.  Go to `http://localhost:5000`.
2.  Enter your input into the chatbox and click 'Send'.
3.  Answer the chatbot's questions.
4.  After completing the conversation, a summary of the conversation will be displayed.

## Structure

-   `app.py`: The main Flask application file.
-   `langchain/`: A directory containing modules used for the OpenAI chat model.
-   `templates/`: A directory containing HTML templates for the Flask application.
-   `static/`: A directory containing static files, such as CSS and JS files.
-   `openai_api.txt`: A text file where you should put your OpenAI API key. This key should not be publicly shared.

