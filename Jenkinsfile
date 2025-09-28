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
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                    source venv/bin/activate
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
