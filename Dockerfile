FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download and verify kernels at build time so runtime needs no network
ENV AL2_KERNEL_DIR=/app/kernels
RUN python scripts/bootstrap_kernels.py

EXPOSE 5000
CMD ["python", "app.py"]
