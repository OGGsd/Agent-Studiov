# Agent Studio

[![License](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)

Agent Studio is a powerful tool for building and deploying AI-powered agents and workflows. With our intuitive interface, you can create sophisticated AI applications without writing complex code.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/OGGsd/agent-studio.git
cd agent-studio
```

2. **Create a virtual environment**
```bash
# Using Python venv
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -e .
```

4. **Run the application**
```bash
axie-studio run
```

5. **Access the application**
Open your browser and navigate to: http://localhost:7860

### 🐳 Docker Development

1. **Build the Docker image**
```bash
docker build -t agent-studio .
```

2. **Run the container**
```bash
docker run -p 7860:7860 agent-studio
```

## 🌐 Production Deployment (DigitalOcean)

### Option 1: App Platform Deployment

1. **Prerequisites**
- A DigitalOcean account
- Docker Hub account
- Your code pushed to GitHub (OGGsd/agent-studio)

2. **Push to Docker Hub**
```bash
docker build -t oggsd/agent-studio:latest .
docker push oggsd/agent-studio:latest
```

3. **Deploy on DigitalOcean App Platform**
- Go to DigitalOcean App Platform
- Click "Create App"
- Choose "Container Image" as source
- Enter Docker Hub image: `oggsd/agent-studio:latest`
- Configure Environment Variables:
  ```
  AXIE_STUDIO_HOST=0.0.0.0
  AXIE_STUDIO_PORT=7860
  ```
- Set HTTP port to 7860
- Deploy your app

### Option 2: Manual Deployment on Droplet

1. **Create a Droplet**
- Choose Ubuntu 22.04 LTS
- Minimum 4GB RAM recommended

2. **SSH into your Droplet**
```bash
ssh root@your-droplet-ip
```

3. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

4. **Pull and Run the Container**
```bash
docker pull oggsd/agent-studio:latest
docker run -d -p 80:7860 oggsd/agent-studio:latest
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| AXIE_STUDIO_HOST | Host to bind the server | 0.0.0.0 |
| AXIE_STUDIO_PORT | Port to run the server | 7860 |
| AXIE_STUDIO_DATABASE_URL | Database connection string (optional) | sqlite:///./axie_studio.db |

## 🛠️ Features

- **Visual Builder Interface**: Drag-and-drop interface for creating AI workflows
- **AI Components**: Pre-built components for various AI tasks
- **Custom Solutions**: Design and deploy your own AI-powered solutions
- **API Integration**: Built-in API server for integration with other applications

## 📚 Documentation

For more detailed information about using Agent Studio, please refer to our [documentation](https://docs.axie-studio.org).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

