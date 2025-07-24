# 🎯 Axie Studio - Professional AI Workflow Platform

[![License](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/OGGsd/Agent-Studiov)

**Axie Studio** is a professional-grade, visual AI workflow platform built on the proven foundation of Langflow. Create sophisticated **AI Agents**, **RAG Systems**, **Chatbots**, and **Complex Workflows** with our intuitive drag-and-drop interface - no coding required!

## ✨ What You Can Build

🤖 **AI Agents** - Autonomous agents that can reason, plan, and execute tasks
📚 **RAG Systems** - Retrieval-Augmented Generation for document Q&A
💬 **Chatbots** - Intelligent conversational interfaces
🔗 **Workflows** - Complex multi-step AI processes
🧠 **LLM Chains** - Sophisticated language model pipelines
📊 **Data Processing** - AI-powered data analysis and transformation
🔍 **Search Systems** - Semantic search and knowledge retrieval
⚡ **API Endpoints** - Deploy your AI workflows as REST APIs

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for frontend development)
- Git

### 🖥️ Local Development

1. **Clone the repository**
```bash
git clone https://github.com/OGGsd/Agent-Studiov.git
cd Agent-Studiov
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3. **Install Axie Studio**
```bash
# Install from source
pip install -e ./src/backend/base

# Or install dependencies manually
cd src/backend/base
pip install -e .
```

4. **Run Axie Studio**
```bash
# New command (recommended)
python -m axie_studio run

# Legacy command (still works)
python -m langflow run

# Or use the CLI directly
axie_studio run --host 0.0.0.0 --port 7860
```

5. **Access the application**
Open your browser and navigate to: **http://localhost:7860**

### 🎯 First Steps
1. **Login** with the default admin account (see Authentication section)
2. **Explore Templates** - Start with pre-built AI Agent and RAG examples
3. **Create Your First Workflow** - Drag and drop components to build AI systems
4. **Test & Deploy** - Run your workflows and deploy as APIs

### 🐳 Docker Development

1. **Build the Docker image**
```bash
docker build -t axie-studio .
```

2. **Run the container**
```bash
docker run -p 7860:7860 axie-studio
```

3. **Access the application**
Navigate to: **http://localhost:7860**

## 🏗️ Core Features & Capabilities

### 🤖 AI Agents
Build autonomous AI agents that can:
- **Reason and Plan** - Multi-step problem solving
- **Use Tools** - Integration with external APIs and services
- **Memory Management** - Persistent conversation history
- **Custom Behaviors** - Define agent personalities and goals

### 📚 RAG (Retrieval-Augmented Generation)
Create powerful document Q&A systems:
- **Document Ingestion** - PDF, TXT, DOCX, CSV support
- **Vector Databases** - Pinecone, Chroma, FAISS integration
- **Semantic Search** - Find relevant information automatically
- **Context-Aware Responses** - Generate answers based on your documents

### 💬 Chatbots & Conversational AI
Design intelligent chat interfaces:
- **Multi-turn Conversations** - Context-aware dialogue
- **Custom Personalities** - Define bot behavior and tone
- **Integration Ready** - Deploy to websites, Slack, Discord
- **Memory & History** - Persistent conversation state

### 🔗 Complex Workflows
Build sophisticated AI pipelines:
- **Visual Flow Builder** - Drag-and-drop interface
- **Conditional Logic** - If/then/else branching
- **Data Transformation** - Process and manipulate data
- **API Integration** - Connect to external services

### 🧠 LLM Integration
Support for all major language models:
- **OpenAI** - GPT-4, GPT-3.5, GPT-4o
- **Anthropic** - Claude 3.5 Sonnet, Claude 3 Opus
- **Google** - Gemini Pro, PaLM
- **Open Source** - Llama, Mistral, CodeLlama
- **Local Models** - Ollama, LM Studio integration

## 🔐 Authentication & User Management

### Commercial Account System
Axie Studio includes a professional account management system:

**Pre-configured Accounts (600 total):**
- **Starter Tier** (200 accounts) - Basic features, limited workflows
- **Professional Tier** (200 accounts) - Advanced features, unlimited workflows
- **Enterprise Tier** (200 accounts) - Full features, priority support

### Admin Features
- **Account Management** - Create, edit, and manage user accounts
- **Tier Control** - Assign and modify user tiers
- **Usage Monitoring** - Track user activity and resource usage
- **Admin Override** - Administrative controls and settings

### Default Login
```
Username: admin
Password: admin
```
*Change default credentials immediately in production!*

## 🌐 Production Deployment

### Option 1: DigitalOcean App Platform

1. **Prerequisites**
- DigitalOcean account
- Docker Hub account
- GitHub repository access

2. **Build and Push Docker Image**
```bash
# Build the image
docker build -t oggsd/axie-studio:latest .

# Push to Docker Hub
docker push oggsd/axie-studio:latest
```

3. **Deploy on App Platform**
- Go to DigitalOcean App Platform
- Click "Create App"
- Choose "Container Image" source
- Image: `oggsd/axie-studio:latest`
- Configure Environment Variables:
  ```
  AXIE_STUDIO_HOST=0.0.0.0
  AXIE_STUDIO_PORT=7860
  AXIE_STUDIO_DATABASE_URL=postgresql://user:pass@host:port/db
  ```
- Set HTTP port to 7860
- Deploy your app

### Option 2: VPS/Droplet Deployment

1. **Create Server**
- Ubuntu 22.04 LTS
- Minimum 4GB RAM (8GB+ recommended)
- 50GB+ storage

2. **Server Setup**
```bash
# SSH into server
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

3. **Deploy Application**
```bash
# Pull and run
docker pull oggsd/axie-studio:latest
docker run -d \
  --name axie-studio \
  -p 80:7860 \
  -e AXIE_STUDIO_HOST=0.0.0.0 \
  -e AXIE_STUDIO_PORT=7860 \
  -v axie_data:/app/data \
  oggsd/axie-studio:latest
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AXIE_STUDIO_HOST` | Host to bind the server | `0.0.0.0` |
| `AXIE_STUDIO_PORT` | Port to run the server | `7860` |
| `AXIE_STUDIO_DATABASE_URL` | Database connection string | `sqlite:///./axie_studio.db` |
| `AXIE_STUDIO_LOG_LEVEL` | Logging level | `info` |
| `AXIE_STUDIO_AUTO_LOGIN` | Enable auto-login | `false` |
| `AXIE_STUDIO_COMPONENTS_PATH` | Custom components directory | `None` |
| `AXIE_STUDIO_CACHE` | Cache type (InMemoryCache, SQLiteCache) | `SQLiteCache` |

### Legacy Compatibility
For backward compatibility, legacy `LANGFLOW_*` environment variables are still supported but deprecated.

## 🛠️ Advanced Usage

### Custom Components
Create your own AI components:
```python
from axie_studio.custom import Component
from axie_studio.io import Output, Input

class MyCustomComponent(Component):
    display_name = "My Custom Component"
    description = "A custom AI component"

    inputs = [
        Input(name="input_text", display_name="Input Text")
    ]
    outputs = [
        Output(name="output_text", display_name="Output Text")
    ]

    def build(self, input_text: str) -> str:
        # Your custom logic here
        return f"Processed: {input_text}"
```

### API Usage
Deploy workflows as REST APIs:
```python
import requests

# Run a workflow via API
response = requests.post(
    "http://localhost:7860/api/v1/run/your-flow-id",
    json={
        "input_value": "Hello, world!",
        "input_type": "chat",
        "output_type": "chat"
    }
)

result = response.json()
```

### Programmatic Usage
Use Axie Studio in your Python code:
```python
from axie_studio.load import run_flow_from_json

# Load and run a workflow
result = run_flow_from_json(
    flow="path/to/your/workflow.json",
    input_value="Your input here"
)
```

## 🔄 Migration from Langflow

Axie Studio is fully compatible with existing Langflow projects:

1. **Import Existing Flows** - All Langflow JSON files work directly
2. **Legacy Code Support** - Existing `langflow` imports continue to work
3. **Database Migration** - Automatic migration from `langflow.db` to `axie_studio.db`
4. **Environment Variables** - Both old and new variable names supported

```python
# These imports still work (with deprecation warnings)
from langflow.graph import Graph
from langflow.load import run_flow_from_json

# New recommended imports
from axie_studio.graph import Graph
from axie_studio.load import run_flow_from_json
```

## 📊 Use Cases & Examples

### 🤖 AI Agent Example
```json
{
  "name": "Customer Support Agent",
  "description": "AI agent that handles customer inquiries",
  "components": [
    "OpenAI GPT-4",
    "Memory Buffer",
    "Tool Calling",
    "Response Generator"
  ]
}
```

### 📚 RAG System Example
```json
{
  "name": "Document Q&A System",
  "description": "Answer questions based on uploaded documents",
  "components": [
    "Document Loader",
    "Text Splitter",
    "Vector Store",
    "Retriever",
    "QA Chain"
  ]
}
```

### 💬 Chatbot Example
```json
{
  "name": "Company Chatbot",
  "description": "Intelligent chatbot for website integration",
  "components": [
    "Chat Input",
    "Conversation Memory",
    "LLM Chain",
    "Chat Output"
  ]
}
```

## 🆚 Comparison with Original Langflow

| Feature | Langflow | Axie Studio |
|---------|----------|-------------|
| **Core Functionality** | ✅ Full | ✅ **100% Compatible** |
| **Visual Workflow Builder** | ✅ Yes | ✅ **Enhanced UI** |
| **AI Agents** | ✅ Yes | ✅ **Advanced Templates** |
| **RAG Systems** | ✅ Yes | ✅ **Optimized Components** |
| **LLM Integration** | ✅ Yes | ✅ **Extended Support** |
| **Commercial Features** | ❌ No | ✅ **User Management** |
| **Account Tiers** | ❌ No | ✅ **Starter/Pro/Enterprise** |
| **Admin Panel** | ❌ No | ✅ **Full Admin Control** |
| **Pre-configured Accounts** | ❌ No | ✅ **600 Ready Accounts** |
| **Professional Branding** | ❌ No | ✅ **Axie Studio Brand** |
| **Legacy Compatibility** | N/A | ✅ **100% Backward Compatible** |

## 📚 Documentation & Resources

- **Official Documentation**: [docs.axie-studio.org](https://docs.axie-studio.org)
- **API Reference**: [api.axie-studio.org](https://api.axie-studio.org)
- **Community Forum**: [community.axie-studio.org](https://community.axie-studio.org)
- **Video Tutorials**: [youtube.com/axie-studio](https://youtube.com/axie-studio)
- **GitHub Repository**: [github.com/OGGsd/Agent-Studiov](https://github.com/OGGsd/Agent-Studiov)

## 🤝 Contributing

We welcome contributions to Axie Studio! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/OGGsd/Agent-Studiov.git
cd Agent-Studiov

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Start development server
python -m axie_studio run --dev
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Axie Studio is built on the foundation of [Langflow](https://github.com/langflow-ai/langflow), an amazing open-source project. We maintain 100% compatibility while adding commercial features and professional branding.

---

**Ready to build your next AI application?** 🚀
[Get Started Now](https://github.com/OGGsd/Agent-Studiov) | [View Documentation](https://docs.axie-studio.org) | [Join Community](https://community.axie-studio.org)

