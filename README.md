# Astrology Backend

## Project Overview
This project is the backend service for an astrology application. It provides API endpoints to generate astrology readings based on user input. The backend is built with Python and Flask, and includes templates for rendering results.

## Setup

### Environment Variables
This project uses [direnv](https://direnv.net/) to manage environment variables. Copy the example environment file and customize it:

```bash
cp .envrc.example .envrc
```

Then edit `.envrc` to add your environment variables. Direnv will automatically load these variables when you enter the project directory.

## Run Instructions

To run the application locally:

```bash
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

| Endpoint       | Method | Description                          |
|----------------|--------|------------------------------------|
| `/`            | GET    | Home page with input form           |
| `/result`      | POST   | Submit data and get astrology result|

## Optional: Cloudflared Setup

To expose your local server securely over the internet using Cloudflared:

1. Install Cloudflared from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation
2. Run the tunnel:

```bash
cloudflared tunnel --url http://localhost:5000
```

3. Use the provided public URL to access your local server remotely.

## Basic Deploy Steps for Render

1. Connect your GitHub repository to Render.
2. Create a new Web Service on Render.
3. Set the build command to:

```bash
pip install -r requirements.txt
```

4. Set the start command to:

```bash
python app.py
```

5. Add environment variables in Render's dashboard as needed.
6. Deploy the service.

## Roadmap

- [ ] Add user authentication
- [ ] Expand astrology reading features
- [ ] Add database support for user data
- [ ] Improve frontend integration
- [ ] Add automated tests and CI/CD pipeline
