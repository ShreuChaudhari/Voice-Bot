#!/bin/bash

# Create and activate virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Streamlit
streamlit run main.py --server.port $PORT --server.address 0.0.0.0
