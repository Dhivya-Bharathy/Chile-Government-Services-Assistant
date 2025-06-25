# Chile Government Services Assistant

An AI-powered assistant that helps users find information about Chilean government services and procedures.

## Features

- **Intelligent Conversational Assistant**: Interacts with users in natural language to resolve queries about ChileAtiende procedures and services.
- **Firecrawl Integration**: Uses Firecrawl to perform real-time searches on the ChileAtiende site and extract relevant information.
- **Session-Based Memory**: The agent remembers the conversation context during the user's current session.
- **Elderly-Friendly Interface**: Clean frontend design with good readability and easy navigation.

## Environment Variables

To run this application, you need to set the following environment variables:

### Required Environment Variables:

1. **FIRECRAWL_API_KEY**: Your Firecrawl API key for web scraping functionality
   - Get it from: https://firecrawl.dev/
   - Example: `FIRECRAWL_API_KEY=your_firecrawl_api_key_here`

2. **SECRET_KEY**: A secure secret key for Flask sessions
   - Generate a secure random string
   - Example: `SECRET_KEY=your_very_long_and_secure_secret_string_here`

### Optional Environment Variables:

3. **FLASK_DEBUG**: Set to "True" for development, "False" for production
   - Example: `FLASK_DEBUG=False`

4. **PORT**: The port number for the application (default: 5000)
   - Example: `PORT=8080`

## Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dhivya-Bharathy/Chile-Government-Services-Assistant.git
   cd Chile-Government-Services-Assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   Create a `.env` file in the root directory:
   ```env
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   SECRET_KEY=your_very_long_and_secure_secret_string_here
   FLASK_DEBUG=True
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Deployment

### Heroku Deployment

1. **Create a Heroku app**:
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**:
   ```bash
   heroku config:set FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   heroku config:set SECRET_KEY=your_very_long_and_secure_secret_string_here
   heroku config:set FLASK_DEBUG=False
   ```

3. **Deploy**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

### Railway Deployment

1. **Connect your GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**:
   - `FIRECRAWL_API_KEY`
   - `SECRET_KEY`
   - `FLASK_DEBUG=False`

### Render Deployment

1. **Connect your GitHub repository to Render**
2. **Set environment variables in Render dashboard**:
   - `FIRECRAWL_API_KEY`
   - `SECRET_KEY`
   - `FLASK_DEBUG=False`

## API Endpoints

- `GET /`: Main application interface
- `POST /api/chat`: Chat API endpoint for sending messages

## Technologies Used

- **Python**: Main programming language
- **Flask**: Web microframework for the backend
- **PraisonAI**: Framework for creating AI agents
- **Firecrawl SDK**: For interacting with the Firecrawl service
- **HTML, CSS, JavaScript**: For the chat user interface
- **SQLite**: For agent session storage

## License

This project is licensed under the MIT License. 