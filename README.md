# EventHub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EventHub is a Flask-based web application designed to help users discover local events — from concerts and food festivals to art shows and community meetups. It offers event search by keywords, city, state, and date, with a sleek, user-friendly interface and integrated features like user profiles, RSVPs, and favorites.

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Docker & Deployment](#docker--deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Event Search:** Filter events by keyword, city, state, and date.
- **User Authentication:** Register, login, and manage user profiles.
- **Favorites & RSVPs:** Users can favorite events and RSVP to them.
- **Responsive UI:** Built with Bootstrap and Bootswatch Solar theme for a modern look.
- **Image Carousel:** Showcases event scenes from around the world.
- **Autocomplete City Search:** Typeahead suggestions for cities to improve user search.
- **Database:** PostgreSQL backend with SQLAlchemy ORM.
- **Dockerized:** Easily deploy with Docker Compose for local and cloud setups.

---

## Demo

*Include a screenshot or link to a live demo if available.*

---

## Tech Stack

- Python 3.11
- Flask (Web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Docker & Docker Compose (Containerization)
- Bootstrap 5 with Bootswatch Solar (Styling)
- JavaScript (Frontend enhancements)

---

## Getting Started

### Prerequisites

- Docker & Docker Compose installed ([Install Docker](https://docs.docker.com/get-docker/))
- Git installed
- Optional: Python 3.11 and virtualenv for local development without Docker

---

## Installation

### Clone the repo

```bash
git clone https://github.com/DeepikaChinnathambi/tcss506_final_project.git
cd tcss506_final_project
```

### Running with Docker Compose (recommended)

```bash
docker compose up --build
```

This command builds and starts the PostgreSQL database and Flask app containers.

### Running Locally without Docker

1. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set environment variables (Linux/Mac):**

    ```bash
    export FLASK_APP=app
    export FLASK_ENV=development
    export SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/postgres
    ```

4. **Run Flask:**

    ```bash
    flask run
    ```

---

## Usage

- Open your browser at [http://localhost:5000](http://localhost:5000) (or your EC2 instance IP)
- Use the search form to find events by keyword, city, state, and date.
- Register/login to save favorite events and RSVP.
- Navigate through the event carousel for featured scenes.

---

## Configuration

- **Database:** By default, connects to a local PostgreSQL instance (or Docker container).
- **Environment Variables:**
    - `FLASK_APP`: Flask entrypoint (default: app)
    - `FLASK_ENV`: Development or production mode
    - `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection URI
- **API Keys:**  
  If you add optional features like Google Maps or Autocomplete, store API keys securely (e.g., `.env` file or AWS Secrets Manager).

---

## Docker & Deployment

The project uses a `Dockerfile` for the Flask app and a `docker-compose.yml` file to orchestrate the Flask app and PostgreSQL database.

**To deploy on AWS EC2:**

1. SSH into your EC2 instance
2. Install Docker and Docker Compose
3. Clone your repo
4. Run:

    ```bash
    docker compose up --build -d
    ```

5. Configure your security group to allow inbound traffic on port 5000 (or your chosen port)

---

## Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- Liam Wilkenson
- Deepika Chinnathambi
- Ainsley Yoshizumi