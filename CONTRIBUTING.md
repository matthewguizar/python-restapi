# CONTRIBUTING

## How to run the dockerfile locally

```
docker build -t IMAGE_NAME 
docker run -dp 5005:5000 -w /app "(path):/app" IMAGE-NAME sh -c "flask run"
```