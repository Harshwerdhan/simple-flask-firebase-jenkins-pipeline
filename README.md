# Flask Firebase Application with CI/CD Pipelines

This repository contains a Python Flask web application with Firebase authentication integration, featuring both Jenkins CI/CD and GitHub Actions workflows for automated testing and deployment.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Application Features](#application-features)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Jenkins CI/CD Pipeline](#jenkins-cicd-pipeline)
- [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
- [Environment Configuration](#environment-configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🚀 Project Overview

This is a Python web application that implements:
- User registration and authentication using Firebase
- Login/logout functionality
- Dashboard with user management
- Comprehensive test suite using pytest
- Automated CI/CD pipelines for testing and deployment

## ✨ Application Features

- **User Authentication**: Secure user registration and login using Firebase Auth
- **Session Management**: Flask session-based user management
- **User Dashboard**: Admin dashboard showing registered users
- **Responsive UI**: Clean, modern web interface
- **Security**: Environment-based configuration for sensitive data
- **Testing**: Comprehensive unit tests for all endpoints

## 🛠 Prerequisites

Before setting up the application, ensure you have:

- **Python 3.8+** installed
- **Firebase Project** with Authentication enabled
- **Firebase Service Account** key file
- **Jenkins Server** (for Jenkins CI/CD)
- **Docker** (optional, for containerized deployment)
- **Git** for version control

## 🏠 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git
cd simple-flask-firebase-jenkins-pipeline
```

### 2. Create Virtual Environment

```bash
python3 -m venv flask-firebase-app
source flask-firebase-app/bin/activate  # On Windows: flask-firebase-app\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
FLASK_SECRET_KEY=your-secret-key-here
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_MEASUREMENT_ID=your-measurement-id
FIREBASE_SERVICE_ACCOUNT=path/to/service-account-key.json
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔧 Jenkins CI/CD Pipeline

### Pipeline Overview

The Jenkins pipeline automates the complete CI/CD process with the following stages:

1. **Checkout**: Pull code from GitHub repository
2. **Validate Environment**: Verify required environment variables
3. **Setup Python Environment**: Create virtual environment and install dependencies
4. **Code Quality Checks**: Run linting and unit tests
5. **Build Docker Image**: Create containerized application
6. **Deploy Application**: Deploy to staging/production environment

### Jenkins Setup

#### 1. Install Jenkins

```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

#### 2. Configure Jenkins

1. Access Jenkins at `http://your-server:8080`
2. Install required plugins:
   - Pipeline
   - Git
   - Docker Pipeline
   - Email Extension
   - Credentials Binding

#### 3. Configure Credentials

Add the following credentials in Jenkins:

- `FLASK_SECRET_KEY`: Your Flask secret key
- `FIREBASE_API_KEY`: Firebase API key
- `FIREBASE_AUTH_DOMAIN`: Firebase auth domain
- `FIREBASE_DATABASE_URL`: Firebase database URL
- `FIREBASE_PROJECT_ID`: Firebase project ID
- `FIREBASE_STORAGE_BUCKET`: Firebase storage bucket
- `FIREBASE_MESSAGING_SENDER_ID`: Firebase messaging sender ID
- `FIREBASE_APP_ID`: Firebase app ID
- `FIREBASE_MEASUREMENT_ID`: Firebase measurement ID
- `FIREBASE_SERVICE_ACCOUNT`: Firebase service account JSON

#### 4. Create Pipeline Job

1. Click "New Item" → "Pipeline"
2. Configure:
   - **Pipeline script from SCM**: Git
   - **Repository URL**: `https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git`
   - **Branch**: `main`
   - **Script Path**: `Jenkinsfile`

### Pipeline Triggers

The pipeline is configured to trigger:
- **On Push**: Automatically when changes are pushed to the main branch
- **Manual**: On-demand execution
- **Scheduled**: Optional scheduled builds

### Pipeline Stages Details

#### Stage 1: Checkout
```groovy
stage('Checkout') {
    steps {
        script {
            echo "Checking out branch: ${params.BRANCH}"
            checkout scm: [
                $class: 'GitSCM',
                branches: [[name: "*/${params.BRANCH}"]],
                userRemoteConfigs: [[
                    url: 'https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git'
                ]]
            ]
        }
    }
}
```

#### Stage 2: Validate Environment
```groovy
stage('Validate Environment') {
    steps {
        script {
            echo "Validating environment variables..."
            def requiredVars = [
                'FLASK_SECRET_KEY', 'FIREBASE_API_KEY', 'FIREBASE_PROJECT_ID'
            ]
            
            requiredVars.each { var ->
                if (!env."${var}") {
                    error "Required environment variable ${var} is not set"
                }
            }
        }
    }
}
```

#### Stage 3: Setup Python Environment
```groovy
stage('Setup Python Environment') {
    steps {
        script {
            echo "Setting up Python virtual environment..."
            sh '''
                # Remove existing virtual environment if it exists
                rm -rf ${VENV_NAME} || true
                
                # Create new virtual environment
                python3 -m venv ${VENV_NAME}
                
                # Activate virtual environment and install dependencies
                source ${VENV_NAME}/bin/activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                
                # Verify installation
                pip list
            '''
        }
    }
}
```

#### Stage 4: Code Quality Checks
```groovy
stage('Code Quality Checks') {
    when {
        expression { params.RUN_TESTS }
    }
    steps {
        script {
            echo "Running code quality checks..."
            sh '''
                source ${VENV_NAME}/bin/activate
                
                # Run tests
                pytest tests/ -v --tb=short --maxfail=3
            '''
        }
    }
}
```

#### Stage 5: Build Docker Image
```groovy
stage('Build Docker Image') {
    steps {
        script {
            echo "Building Docker image..."
            sh '''
                # Build Docker image
                docker build -t flask-firebase-app:${BUILD_NUMBER} .
                
                # Tag as latest
                docker tag flask-firebase-app:${BUILD_NUMBER} flask-firebase-app:latest
            '''
        }
    }
}
```

#### Stage 6: Deploy Application
```groovy
stage('Deploy Application') {
    when {
        expression { params.DEPLOY }
    }
    steps {
        script {
            echo "Deploying application..."
            sh '''
                # Stop existing container if running
                docker stop flask-app || true
                docker rm flask-app || true
                
                # Run new container
                docker run -d \
                    --name flask-app \
                    --restart unless-stopped \
                    -p ${APP_PORT}:5000 \
                    -e FLASK_SECRET_KEY="${FLASK_SECRET_KEY}" \
                    -e FIREBASE_API_KEY="${FIREBASE_API_KEY}" \
                    -e FIREBASE_AUTH_DOMAIN="${FIREBASE_AUTH_DOMAIN}" \
                    -e FIREBASE_DATABASE_URL="${FIREBASE_DATABASE_URL}" \
                    -e FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID}" \
                    -e FIREBASE_STORAGE_BUCKET="${FIREBASE_STORAGE_BUCKET}" \
                    -e FIREBASE_MESSAGING_SENDER_ID="${FIREBASE_MESSAGING_SENDER_ID}" \
                    -e FIREBASE_APP_ID="${FIREBASE_APP_ID}" \
                    -e FIREBASE_MEASUREMENT_ID="${FIREBASE_MEASUREMENT_ID}" \
                    -e FIREBASE_SERVICE_ACCOUNT="${FIREBASE_SERVICE_ACCOUNT}" \
                    flask-firebase-app:latest
                
                # Wait for application to start
                sleep 10
                
                # Health check
                curl -f http://localhost:${APP_PORT}/ || exit 1
            '''
        }
    }
}
```

### Jenkins Notifications

Configure email notifications in Jenkins:

1. Go to **Manage Jenkins** → **Configure System**
2. Set up SMTP server details
3. Configure email templates for success/failure notifications

## 🚀 GitHub Actions CI/CD Pipeline

### Workflow Overview

GitHub Actions provides automated CI/CD with the following jobs:

1. **Install Dependencies**: Install Python dependencies
2. **Run Tests**: Execute test suite using pytest
3. **Build**: Prepare application for deployment
4. **Deploy to Staging**: Deploy when changes are pushed to staging branch
5. **Deploy to Production**: Deploy when a release is tagged

### Workflow Configuration

The workflow is defined in `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, staging ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --tb=short
    
    - name: Run linting
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/staging'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment..."
        # Add your staging deployment commands here
    
    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production environment..."
        # Add your production deployment commands here
    
    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#deployments'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Secrets Configuration

Configure the following secrets in your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `FLASK_SECRET_KEY`
   - `FIREBASE_API_KEY`
   - `FIREBASE_AUTH_DOMAIN`
   - `FIREBASE_DATABASE_URL`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_STORAGE_BUCKET`
   - `FIREBASE_MESSAGING_SENDER_ID`
   - `FIREBASE_APP_ID`
   - `FIREBASE_MEASUREMENT_ID`
   - `FIREBASE_SERVICE_ACCOUNT`

### Workflow Triggers

- **Push to main**: Runs tests and code quality checks
- **Push to staging**: Runs tests and deploys to staging
- **Release published**: Runs tests and deploys to production
- **Pull Request**: Runs tests for code review

## 🧪 Testing

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_app.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

The test suite covers:
- Page loading functionality
- Authentication flows
- Session management
- Error handling

### Test Structure

```
tests/
├── __init__.py
└── test_app.py
    ├── test_register_page_loads()
    ├── test_login_page_loads()
    └── test_dashboard_redirects_if_not_logged_in()
```

## 🚀 Deployment

### Docker Deployment

1. **Build Docker Image**:
```bash
docker build -t flask-firebase-app .
```

2. **Run Container**:
```bash
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  -e FLASK_SECRET_KEY="your-secret-key" \
  -e FIREBASE_API_KEY="your-api-key" \
  # ... other environment variables
  flask-firebase-app
```

### Production Deployment

1. **Set Environment Variables**:
```bash
export FLASK_ENV=production
export FLASK_SECRET_KEY="your-production-secret-key"
# ... other variables
```

2. **Run Application**:
```bash
python app.py
```

## 📸 Screenshots

### Jenkins Pipeline Screenshots

#### Pipeline Overview
![Jenkins Pipeline Overview](screenshots/jenkins-pipeline-overview.png)

#### Build Stage
![Jenkins Build Stage](screenshots/jenkins-build-stage.png)

#### Test Stage
![Jenkins Test Stage](screenshots/jenkins-test-stage.png)

#### Deploy Stage
![Jenkins Deploy Stage](screenshots/jenkins-deploy-stage.png)

### GitHub Actions Screenshots

#### Workflow Overview
![GitHub Actions Overview](screenshots/github-actions-overview.png)

#### Test Job
![GitHub Actions Test Job](screenshots/github-actions-test.png)

#### Deploy Job
![GitHub Actions Deploy Job](screenshots/github-actions-deploy.png)

## 🔧 Troubleshooting

### Common Issues

#### 1. Firebase Authentication Errors
- **Issue**: Firebase authentication not working
- **Solution**: Verify Firebase configuration and service account key

#### 2. Jenkins Build Failures
- **Issue**: Pipeline fails during dependency installation
- **Solution**: Check Python version and virtual environment setup

#### 3. GitHub Actions Failures
- **Issue**: Workflow fails due to missing secrets
- **Solution**: Verify all required secrets are configured

#### 4. Docker Build Issues
- **Issue**: Docker image build fails
- **Solution**: Check Dockerfile syntax and base image availability

### Debug Commands

```bash
# Check Jenkins logs
sudo journalctl -u jenkins -f

# Check Docker containers
docker ps -a
docker logs flask-app

# Check application logs
tail -f /var/log/flask-app.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: [your-email@example.com]

## 🔗 Repository Links

- **GitHub Repository**: https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline
- **Jenkins Server**: [Your Jenkins Server URL]
- **Staging Environment**: [Your Staging URL]
- **Production Environment**: [Your Production URL]

---

**Note**: This documentation covers both Jenkins CI/CD and GitHub Actions workflows as required by the assignment. Make sure to replace placeholder URLs and configuration details with your actual values.