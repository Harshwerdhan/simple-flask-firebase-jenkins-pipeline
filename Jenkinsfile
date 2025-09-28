pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'staging', description: 'Git branch to build')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy to production')
    }
    
    environment {
        // Flask configuration
        FLASK_SECRET_KEY = credentials('FLASK_SECRET_KEY')
        FLASK_ENV = 'production'
        
        // Firebase configuration
        FIREBASE_API_KEY = credentials('FIREBASE_API_KEY')
        FIREBASE_AUTH_DOMAIN = credentials('FIREBASE_AUTH_DOMAIN')
        FIREBASE_DATABASE_URL = credentials('FIREBASE_DATABASE_URL')
        FIREBASE_PROJECT_ID = credentials('FIREBASE_PROJECT_ID')
        FIREBASE_STORAGE_BUCKET = credentials('FIREBASE_STORAGE_BUCKET')
        FIREBASE_MESSAGING_SENDER_ID = credentials('FIREBASE_MESSAGING_SENDER_ID')
        FIREBASE_APP_ID = credentials('FIREBASE_APP_ID')
        FIREBASE_MEASUREMENT_ID = credentials('FIREBASE_MEASUREMENT_ID')
        FIREBASE_SERVICE_ACCOUNT = credentials('FIREBASE_SERVICE_ACCOUNT')
        
        // Application configuration
        APP_PORT = '5000'
        VENV_NAME = 'flask-firebase-app'
    }
    
    stages {
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
        
        stage('Code Quality Checks') {
            when {
                expression { params.RUN_TESTS }
            }
            steps {
                script {
                    echo "Running code quality checks..."
                    sh '''
                        source ${VENV_NAME}/bin/activate
                        
                        # Run linting (if you add flake8 or similar)
                        # flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
                        
                        # Run tests
                        pytest tests/ -v --tb=short --maxfail=3
                    '''
                }
            }
        }
        
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
    }
    
    post {
        always {
            script {
                echo "Pipeline completed with status: ${currentBuild.result ?: 'SUCCESS'}"
                
                // Cleanup
                sh '''
                    # Clean up virtual environment
                    rm -rf ${VENV_NAME} || true
                    
                    # Clean up old Docker images (keep last 5)
                    docker images flask-firebase-app --format "table {{.Tag}}" | tail -n +2 | head -n -5 | xargs -r docker rmi flask-firebase-app: || true
                '''
            }
        }
        
        success {
            echo "Pipeline succeeded! Application deployed successfully."
            // Add notification here (Slack, email, etc.)
        }
        
        failure {
            echo "Pipeline failed! Check the logs for details."
            // Add failure notification here
        }
        
        unstable {
            echo "Pipeline completed with warnings."
        }
    }
}
