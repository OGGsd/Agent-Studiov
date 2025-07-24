FROM axiestudio/axie-studio:1.0-alpha

CMD ["python", "-m", "axie_studio", "run", "--host", "0.0.0.0", "--port", "7860"]
