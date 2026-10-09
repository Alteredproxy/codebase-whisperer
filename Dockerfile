# 1. Start with a blank Linux computer that has Python pre-installed
FROM python:3.11-slim

# 2. Set our working folder inside the blank computer
WORKDIR /app

# 3. Copy our requirements file into the computer
COPY requirements.txt .

# 4. Tell the computer to install the packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all our python files and folders into the computer
COPY . .

# 6. Make our start script executable
RUN chmod +x start.sh

# 7. When the box turns on, run the script!
CMD ["./start.sh"]
