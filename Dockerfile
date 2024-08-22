FROM python:3.11

# 
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update
RUN apt-get install -y firefox-esr curl

COPY . .

RUN chmod +x ./download_geckodriver.sh
RUN ls -l . && ./download_geckodriver.sh

# Expose the port that the FastAPI app runs on
EXPOSE 3000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]