#!/bin/bash

# Download the geckodriver tar.gz file
curl -LO https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz

# Extract the tar.gz file
tar -xzf geckodriver-v0.35.0-linux64.tar.gz

# Optional: Remove the tar.gz file after extraction
rm geckodriver-v0.35.0-linux64.tar.gz