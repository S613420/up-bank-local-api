# Up Bank Local API

A FastAPI-based wrapper for the [Up Bank REST API](https://developer.up.com.au), designed for local execution. This application provides a convenient interface to access both individual and shared Up Bank accounts using multiple API tokens.

## Features

- Support for multiple Up Bank accounts (individual and shared)
- Clean, modular structure for easy maintenance and extension
- Comprehensive error handling and logging
- Interactive API documentation via FastAPI's Swagger UI
- Simple local deployment for personal use

## Prerequisites

- Python 3.11.9 or later
- Up Bank API tokens (obtain from your Up Bank account settings)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd up-bank-local-api
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Using pip and requirements.txt
   pip install -r requirements.txt
   
   # OR using pip and pyproject.toml
   pip install -e .
   ```

3. Create a `.env` file in the project root (based on `.env.example`):
   ```
   # Copy the .env.example file
   cp .env.example .env
   
   # Now edit the .env file and add your tokens
   nano .env  # or use your preferred text editor
   ```
   
   Your `.env` file should contain:
   ```
   # Up Bank API Configuration
   # Personal tokens (REQUIRED)
   USER1_UP_TOKEN=your_token_here
   USER2_UP_TOKEN=your_token_here
   
   # Shared account token (optional)
   SHARED_UP_TOKEN=your_shared_token_here
   
   # API settings
   API_HOST=0.0.0.0
   API_PORT=8000
   LOG_LEVEL=INFO
   ```
   
   To get your Up Bank API tokens:
   1. Log in to your Up Bank account
   2. Go to Settings > API Access
   3. Generate a Personal Access Token
   4. Copy the token and add it to your `.env` file

## Usage

1. Start the API server:
   ```
   python main.py
   ```

2. Access the API documentation at:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

The API provides endpoints for accessing Up Bank data grouped by entity type:

### Accounts
- `GET /api/v1/accounts?account_type={account_type}` - Get all accounts
- `GET /api/v1/accounts/{account_id}?account_type={account_type}` - Get account by ID

### Transactions
- `GET /api/v1/transactions?account_type={account_type}` - Get all transactions
- `GET /api/v1/transactions/{transaction_id}?account_type={account_type}` - Get transaction by ID
- `GET /api/v1/transactions/account/{account_id}?account_type={account_type}` - Get transactions for a specific account

### Categories
- `GET /api/v1/categories?account_type={account_type}` - Get all categories
- `GET /api/v1/categories/{category_id}?account_type={account_type}` - Get category by ID

## Account Types

- `user1` - First user's Up Bank account
- `user2` - Second user's Up Bank account
- `shared` - Shared 2UP account (if configured)

## Development

For development purposes, you can install additional development dependencies:

```
# Using pip and requirements-dev.txt
pip install -r requirements-dev.txt

# OR using pip and pyproject.toml
pip install -e ".[dev]"
```

This will install testing and code formatting tools such as pytest, black, and isort.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Up Bank API Documentation](https://developer.up.com.au)
