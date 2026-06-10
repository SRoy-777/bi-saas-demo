FROM python:3.11

# Set up a new user named "user" with UID 1000
RUN useradd -m -u 1000 user

# Set the working directory to the user's home directory
WORKDIR /home/user/app
ENV SNAPSHOT_DIR=/tmp/snapshot

# Copy and install requirements
COPY --chown=user:user requirements.txt /home/user/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY --chown=user:user . /home/user/app

# Switch to the non-root user
USER user

# Expose the standard Hugging Face Spaces port
EXPOSE 7860

# Run the Dash dashboard app
CMD ["python", "app/app.py"]