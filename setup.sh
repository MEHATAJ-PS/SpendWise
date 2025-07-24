#!/bin/bash

echo "🔧 Creating virtual environment..."
python -m venv venv

echo "📦 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

echo "📚 Installing requirements..."
pip install -r requirements.txt

echo "🚀 Launching SpendWise..."
python main.py
