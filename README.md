<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Niflheim - Home of Mist"></a>
</p>

<h3 align="center">Niflheim</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/julesrubin/niflheim.svg)](https://github.com/julesrubin/niflheim/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/julesrubin/niflheim.svg)](https://github.com/julesrubin/niflheim/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> A unified hosting platform for all of Jules Rubin's projects and services - from portfolios to APIs, all accessible through a single domain.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Project Structure](#project_structure)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

Niflheim is my personal cloud-native hosting platform that I've built to serve as the central hub for all my projects and services. Named after the Norse realm meaning "Home of Mist," I designed this platform to provide a unified entry point where anyone can access my various applications, APIs, and services through a single domain with intelligent routing.

Currently, Niflheim hosts my comprehensive portfolio website showcasing my work as a Data and AI student at EFREI Paris, featuring projects I've developed across web development, machine learning, data analysis, mobile applications, and electronics. However, I've architected Niflheim to be completely flexible - I can deploy any type of service or application here, making it my personal cloud playground.

I've built this entire platform leveraging **Google Cloud Platform's cutting-edge technologies**. The architecture features containerized microservices running on **Google Cloud Run** for serverless scalability, **Google Artifact Registry** for secure container image management, and **Google Cloud Build** for automated CI/CD pipelines. I've implemented infrastructure as code using **Terraform** to manage all GCP resources, including **IAM roles**, **service accounts**, and **Cloud Storage** for state management. The intelligent routing is handled by a Caddy reverse proxy that I've configured to automatically distribute requests across my services, all deployed and managed through **Google Cloud's serverless infrastructure**.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

- Docker and Docker Compose
- Node.js (v18+) and Yarn
- Python (3.13+)
- Google Cloud SDK (for deployment)
- Terraform (for infrastructure)

### Installing

1. Clone the repository:
```bash
git clone https://github.com/julesrubin/niflheim.git
cd niflheim
```

2. Set up the frontend:
```bash
cd frontend/portfolio
yarn install
yarn build:css
```

3. Set up the backend API:
```bash
cd backend/api
pip install -e .
```

4. Build and run with Docker:
```bash
# Build portfolio image
make image portfolio

# Build proxy image  
make image proxy

# Run portfolio locally
make run portfolio

# Run proxy locally
make run proxy
```

## 🔧 Running the tests <a name = "tests"></a>

The project includes automated tests for the React components.

### Frontend Tests

```bash
cd frontend/portfolio
yarn test
```

### Component Tests

The test suite includes:
- Banner component tests
- Modal component tests
- React component integration tests

## 🎈 Usage <a name="usage"></a>

Niflheim serves as my unified platform hosting multiple services:

### Current Services

- **Portfolio (`/portfolio`)**: A comprehensive showcase of my projects including:
  - **Web Applications**: Street Workout Helper, meal planning applications
  - **Machine Learning**: DDoS attack detection, heart failure prediction using SVM
  - **Mobile Development**: GuideMe navigation app
  - **Algorithms**: Finite Automaton simulator, Floyd-Warshall implementation
  - **Electronics**: Microcontroller projects
  - **Data Science**: Wikipedia search engine, various ML projects

- **API (`/api`)**: My FastAPI backend service providing programmatic access to various functionalities

### Platform Features

- **Intelligent Routing**: My Caddy reverse proxy automatically routes requests to appropriate services
- **Unified Domain**: All my services accessible through a single entry point
- **Health Monitoring**: Built-in health checks for all services
- **Scalable Architecture**: I can easily add new services without infrastructure changes

Visit the root domain to explore my portfolio, or access specific services via their designated paths.

## 🚀 Deployment <a name = "deployment"></a>

I've deployed this project on **Google Cloud Platform** using **Cloud Run** services with **Terraform** for infrastructure as code, showcasing my expertise in modern cloud-native DevOps practices.

### Prerequisites for Deployment

1. Delete the config and init directories in gcp and each service directory.

2. Enable the required **Google Cloud APIs** using the following `gcloud` commands (replace `<PROJECT_ID>` with your project ID):

```sh
gcloud services enable cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    secretmanager.googleapis.com \
    cloudresourcemanager.googleapis.com \
    --project=<PROJECT_ID>
```

3. Run my initialization script for each service:

```sh
./scripts/init.sh <PROJECT_ID> <service folder>
```

4. Configure the **2ndGen GitHub connection** in the **GCP Console** (must be named `github_connection`) or you can set the name in the `gcp/repo_connection.tf` file.

### Terraform Deployment

My infrastructure leverages multiple **Google Cloud Platform** services:
- **Google Cloud Run** services for serverless container deployment (frontend, backend, and proxy)
- **Google Artifact Registry** for secure container image storage and versioning
- **Google Cloud Build** for automated CI/CD pipelines with GitHub integration
- **Google Cloud IAM** roles and service accounts for secure access management
- **Google Cloud Storage** for Terraform state management
- **Google Cloud Resource Manager** for project-level resource organization

Deploy using my custom Makefile:
```bash
# Initialize Terraform with GCS backend
make init

# Plan deployment across all GCP services
make plan

# Apply infrastructure to Google Cloud Platform
make apply
```

## ⛏️ Built Using <a name = "built_using"></a>

### Frontend
- [React](https://reactjs.org/) - Frontend Framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework
- [Framer Motion](https://www.framer.com/motion/) - Animation Library
- [React Router](https://reactrouter.com/) - Client-side Routing

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) - Python Web Framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data Validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI Server

### Infrastructure & DevOps
- [Caddy](https://caddyserver.com/) - Reverse Proxy Server
- [Docker](https://www.docker.com/) - Containerization
- [Google Cloud Run](https://cloud.google.com/run) - Serverless Container Platform
- [Terraform](https://www.terraform.io/) - Infrastructure as Code
- [Google Cloud Build](https://cloud.google.com/build) - CI/CD Pipeline

### Tools & Development
- [Nginx](https://nginx.org/) - Web Server
- [PostCSS](https://postcss.org/) - CSS Processing
- [EmailJS](https://www.emailjs.com/) - Email Integration

## 📁 Project Structure <a name = "project_structure"></a>

```
niflheim/
├── frontend/portfolio/          # React portfolio application
├── backend/
│   ├── api/                    # FastAPI backend service
│   └── proxy/                  # Caddy reverse proxy
├── gcp/                        # Terraform infrastructure
│   ├── services/               # Individual service configurations
│   └── modules/                # Reusable Terraform modules
└── scripts/                    # Deployment and utility scripts
```

## ✍️ Authors <a name = "authors"></a>

- **Jules Rubin** - [@julesrubin](https://github.com/julesrubin) - Full-stack development, architecture, and deployment

Data and AI student at EFREI Paris, passionate about technology and sports with over a decade of soccer experience.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- EFREI Paris for providing excellent education in Data Science and AI
- The open-source community for the amazing tools and frameworks
- All the contributors to the technologies used in this project
- Inspiration from modern portfolio designs and best practices
