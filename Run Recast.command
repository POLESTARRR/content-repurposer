#!/bin/bash
# Double-click launcher: sets up a local virtualenv on first run, then
# starts the app and opens it in your browser. Safe to double-click
# again any time, since later launches skip straight to starting the app.
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Setting up Recast (first run only)..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Starting Recast..."
streamlit run app.py
