# DevSecOps Pipeline

A production-style **DevSecOps CI/CD pipeline** that integrates application testing, dependency vulnerability scanning, secure Docker image builds, container security scanning and GitHub Container Registry (GHCR) publishing.

The project demonstrates how security checks can be integrated directly into the software delivery lifecycle so vulnerable dependencies or container images can be detected before deployment.

---

## Architecture

```text
Developer Push / Pull Request
            │
            ▼
      GitHub Actions
            │
            ▼
    Application Testing
            │
            ▼
   Dependency Security Scan
        (pip-audit)
            │
            ▼
       Docker Build
            │
            ▼
      Trivy Image Scan
   Vulnerability + Secrets
            │
            ▼
      Push to GHCR
            │
            ▼
   Secure Container Image
```

---

## Project Highlights

* GitHub Actions DevSecOps pipeline
* Automated Python application testing
* Dependency vulnerability scanning with `pip-audit`
* Docker container security scanning with Trivy
* Secret detection with Trivy
* HIGH and CRITICAL vulnerability blocking
* Secure non-root Docker container
* Minimal Python slim base image
* Debian security package updates during image build
* Kubernetes deployment manifests
* Health and readiness probes
* Resource requests and limits
* Kubernetes security context
* GitHub Container Registry integration
* Automated Docker image publishing
* Pull Request security validation

---

## Technologies

| Technology        | Purpose                                     |
| ----------------- | ------------------------------------------- |
| Python            | Application                                 |
| Flask             | Web framework                               |
| Gunicorn          | Production WSGI server                      |
| Docker            | Containerization                            |
| Kubernetes        | Container orchestration                     |
| GitHub Actions    | CI/CD automation                            |
| pip-audit         | Python dependency security scanning         |
| Trivy             | Container vulnerability and secret scanning |
| GHCR              | Container image registry                    |
| GitHub Codespaces | Development environment                     |

---

## Application

The project contains a lightweight Flask application with several endpoints.

### Main Endpoint

```text
GET /
```

Returns application information including:

* Application name
* Version
* Environment
* Hostname
* Status message

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "timestamp": "2026-09-15T18:00:00+00:00"
}
```

### Readiness Check

```text
GET /ready
```

Used by Kubernetes to determine whether the application is ready to receive traffic.

### API Status

```text
GET /api/v1/status
```

Returns application runtime and environment information.

---

## Repository Structure

```text
devsecops-pipeline/
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
│
├── .github/
│   └── workflows/
│       └── devsecops.yml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

## DevSecOps Pipeline

The GitHub Actions workflow performs security checks automatically.

### 1. Application Testing

The pipeline:

* Installs Python dependencies
* Performs Python syntax validation
* Starts the Flask test application
* Tests the `/health` endpoint

A failed application test stops the pipeline.

---

### 2. Dependency Security Scan

The project uses `pip-audit` to scan Python dependencies for known security vulnerabilities.

```bash
pip-audit -r app/requirements.txt
```

The pipeline is designed to detect vulnerable application dependencies before the Docker image is built.

---

### 3. Docker Image Build

After dependency scanning succeeds, the application is packaged into a Docker image.

The container uses:

```text
python:3.12-slim-bookworm
```

The Dockerfile also updates the underlying Debian packages during the build to reduce exposure to known OS-level vulnerabilities.

---

### 4. Container Security Scan

Trivy scans the resulting Docker image for:

* OS vulnerabilities
* Python package vulnerabilities
* HIGH vulnerabilities
* CRITICAL vulnerabilities
* Exposed secrets

Example:

```bash
trivy image ghcr.io/syedwasifabbas5/devsecops-pipeline:latest
```

The pipeline is configured to fail when HIGH or CRITICAL vulnerabilities are detected.

This means security findings can block an unsafe image from being published.

---

### 5. Push to GitHub Container Registry

Only after the security scan succeeds is the image pushed to GHCR.

Image:

```text
ghcr.io/syedwasifabbas5/devsecops-pipeline:latest
```

GHCR provides centralized storage for the project's container image.

---

## Docker Security

The container follows several security practices.

### Non-root User

The application does not run as root.

```text
UID: 10001
```

### Minimal Base Image

The project uses a slim Python image to reduce unnecessary packages and attack surface.

### Healthcheck

Docker includes an application health check to help detect unhealthy containers.

### Dependency Pinning

Python dependencies are pinned to specific versions in:

```text
app/requirements.txt
```

This provides more predictable and reproducible builds.

---

## Kubernetes Security

The project also includes Kubernetes deployment manifests designed with security and reliability in mind.

The deployment includes:

* 2 application replicas
* Rolling updates
* Health probes
* Readiness probes
* CPU and memory limits
* Non-root execution
* Restricted security settings
* Kubernetes Service
* Dedicated namespace

Namespace:

```text
devsecops
```

Deployment:

```text
devsecops-app
```

---

## Running Locally

### Build the Docker Image

```bash
docker build -t devsecops-pipeline:1.0.0 .
```

### Run the Container

```bash
docker run -d --name devsecops-app -p 8080:8080 devsecops-pipeline:1.0.0
```

### Test the Application

```bash
curl http://localhost:8080/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

## Security Scanning Locally

### Dependency Scan

Install pip-audit:

```bash
pip install pip-audit
```

Run:

```bash
pip-audit -r app/requirements.txt
```

### Docker Image Scan

If Trivy is installed locally:

```bash
trivy image devsecops-pipeline:1.0.0
```

---

## Kubernetes Deployment

Create the namespace and application resources:

```bash
kubectl apply -f k8s/
```

Check the deployment:

```bash
kubectl -n devsecops get deployments
```

Check pods:

```bash
kubectl -n devsecops get pods
```

Check services:

```bash
kubectl -n devsecops get services
```

Check rollout:

```bash
kubectl -n devsecops rollout status deployment/devsecops-app
```

---

## Security Gate

The pipeline follows this security principle:

```text
Code
 ↓
Test
 ↓
Dependency Scan
 ↓
Docker Build
 ↓
Trivy Security Scan
 ↓
Publish Image
```

If a security gate fails, the image should not proceed to the publishing stage.

This demonstrates the concept of **Shift Left Security**, where security checks are performed early in the development lifecycle rather than after deployment.

---

## Vulnerability Remediation Example

During development, the dependency scanner identified vulnerabilities in older package versions.

The vulnerable dependencies were upgraded to patched versions before continuing.

The Docker image scan also identified vulnerabilities originating from the underlying Debian packages.

Instead of bypassing the security scanner, the Docker base image and OS packages were updated until the security scan passed.

This demonstrates a practical DevSecOps remediation workflow:

```text
Detect
  ↓
Investigate
  ↓
Update
  ↓
Rebuild
  ↓
Rescan
  ↓
Pass
```

---

## CI/CD Workflow

The workflow is triggered on:

* Pushes to `main`
* Pull Requests targeting `main`

Pipeline stages:

```text
Test
  ↓
Dependency Scan
  ↓
Docker Build
  ↓
Trivy Scan
  ↓
GHCR Push
```

A failure in an earlier security stage prevents the next stage from running.

---

## What This Project Demonstrates

This project demonstrates practical knowledge of:

* CI/CD automation
* DevSecOps practices
* GitHub Actions
* Docker security
* Container image scanning
* Dependency vulnerability management
* Secret scanning
* Linux container security
* Kubernetes deployment
* GitHub Container Registry
* Security gates
* Vulnerability remediation
* Secure software delivery

---

## Portfolio Value

This project is designed to demonstrate how a DevOps engineer can integrate security into an automated delivery pipeline rather than treating security as a separate manual process.

It complements the other projects in this portfolio by adding the security layer:

```text
Kubernetes
    +
CI/CD
    +
DevSecOps
```

---

## Author

**Syed Wasif Abbas**
