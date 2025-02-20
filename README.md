# Weekend Fun

An AI-powered event recommendation system that finds and suggests personalized weekend events based on your interests.

## Features

- Personalized event discovery based on user interests
- Automatic weekend event filtering
- AI-powered event ranking using OpenAI
- Email notifications with top event recommendations
- Web scraping from popular event websites
- User preference management

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)
- OpenAI API key
- SendGrid API key and verified sender email

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/weekend_fun.git
cd weekend_fun
```

2. Install Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Configure Poetry to create virtual environment in project directory:

```bash
poetry config virtualenvs.in-project true
```

4. Install dependencies:

```bash
poetry install
```

## Configuration

1. Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=your_sender_email@example.com
```

## Usage

Run the application:

```bash
poetry run python main.py
```

The application will:

1. Ask for your information:
   - Name
   - City
   - Email
   - Interests
   Currently, it just reads from a config file.
2. Find events in your city
3. Filter for upcoming weekend events using AI
4. Rank events based on your interests using AI
5. Send you an email with the top recommendations

## Project Structure

```
weekend_fun/
├── __init__.py
├── user_manager.py      # User information handling
├── event_finder.py      # Event discovery and scraping
├── event_ranker.py      # AI-powered event ranking
└── email_sender.py      # Email notification system

tests/
├── __init__.py
├── test_main.py
└── test_event_ranker.py

main.py                  # Application entry point
```

## Deployment

The application is configured to run on Railway:

1. Import the repository to Railway
2. Add your API keys to Railway's Secrets tab:
   - `OPENAI_API_KEY`
   - `SENDGRID_API_KEY`
   - `FROM_EMAIL`
3. The application will automatically use Poetry for dependency management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing GPT models
- SendGrid for email services
- Jina AI for web scraping capabilities
- Railway for deployment
- Event websites for providing event data

