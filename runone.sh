#!/bin/bash

# Set the environment name
ENV_NAME="<env_name>"

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found!"
    exit 1
fi

# Function to check for successful commands
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error occurred during the execution of: $1"
        exit 1
    fi
}

# Function to activate conda environment and run a command
run_with_conda() {
    conda activate "$ENV_NAME"
    check_command "conda activate $ENV_NAME"
    eval "$1"
}

# Step 1: Set up UI
echo "Setting up UI..."
cd ui || exit
npm install
check_command "npm install in ui"
npm run ui &
check_command "npm run ui in ui"

# Step 2: Start Auth Microservice
echo "Starting Auth Microservice..."
cd ../customer-auth || exit
npm install
check_command "npm install in customer-auth"
nodemon server.js &
check_command "nodemon in customer-auth"

# Step 3: Start ATM Locator Microservice
echo "Starting ATM Locator Microservice..."
cd ../atm-locator || exit
npm install
check_command "npm install in atm-locator"
nodemon server.js &
check_command "nodemon in atm-locator"

# Step 4: Create Python Virtual Environment
echo "Creating Python Virtual Environment..."
cd ../dashboard || exit
if ! conda info --envs | grep -q "$ENV_NAME"; then
    conda create --name "$ENV_NAME" -y
    check_command "conda create environment"
fi
run_with_conda "pip install -r requirements.txt"
check_command "pip install in dashboard"

# Step 5: Start Python Microservices
# Accounts Microservice
echo "Starting Accounts Microservice..."
cd ../accounts || exit
run_with_conda "python accounts.py &"
check_command "python accounts.py"

# Transactions Microservice
echo "Starting Transactions Microservice..."
cd ../transactions || exit
run_with_conda "python transaction.py &"
check_command "python transaction.py"

# Loan Microservice
echo "Starting Loan Microservice..."
cd ../loan || exit
run_with_conda "python loan.py &"
check_command "python loan.py"

# Step 6: Start Dashboard Microservice
echo "Starting Dashboard Microservice..."
cd ../dashboard || exit
run_with_conda "python dashboard.py &"
check_command "python dashboard.py"

# Final Step: Access the application
echo "Setup complete! Access the Martian Bank App at http://localhost:3000"
