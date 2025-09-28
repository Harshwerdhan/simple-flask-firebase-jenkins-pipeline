pipeline {
    agent any   // Run on any available Jenkins agent

    stages {
        stage('Checkout') {
            steps {
                // Pull code from your repo
                git branch: 'main', url: 'https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git'
            }
        }

        stage('Set up Python venv') {
            steps {
                sh '''
                    python3 -m venv flask-firebase-app
                    . flask-firebase-app/bin/activate
                    pip install --upgrade pip setuptools
                    pip install -r requirments.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . flask-firebase-app/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                    . flask-firebase-app/bin/activate
                    python app.py
                '''
            }
        }
    }

    post {
        always {
            sh 'deactivate || true'   // make sure venv is deactivated
            echo 'Pipeline finished!'
        }
    }
}
