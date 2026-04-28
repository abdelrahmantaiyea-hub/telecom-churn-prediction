# 1. Use a lightweight Python 3.10 image as the base OS
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (This is a Senior trick to use Docker's cache and make builds 10x faster)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project files into the container
COPY . .

# 6. Expose the port Streamlit uses
EXPOSE 8501

# 7. Tell the container how to run the app when it wakes up
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]