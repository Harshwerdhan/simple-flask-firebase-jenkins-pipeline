pipeline {
    agent any   // Run on any available Jenkins agent

    environment{
        // Setup enviroment variable for firebase
        FLASK_SECRET_KEY=credentials('FLASK_SECRET_KEY')
        FIREBASE_API_KEY=credentials('FIREBASE_API_KEY')
        FIREBASE_AUTH_DOMAIN=credentials('FIREBASE_AUTH_DOMAIN')
        FIREBASE_DATABASE_URL=credentials('FIREBASE_DATABASE_URL')
        FIREBASE_PROJECT_ID=credentials('FIREBASE_PROJECT_ID')
        FIREBASE_STORAGE_BUCKET=credentials('FIREBASE_STORAGE_BUCKET')
        FIREBASE_MESSAGING_SENDER_ID=credentials('FIREBASE_MESSAGING_SENDER_ID')
        FIREBASE_APP_ID=credentials('FIREBASE_APP_ID')
        FIREBASE_MEASUREMENT_ID=credentials('FIREBASE_MEASUREMENT_ID')
        FIREBASE_SERVICE_ACCOUNT=credentials('FIREBASE_SERVICE_ACCOUNT')
    }

    

    stages {
        stage('Checkout') {
            steps {
                // Pull code from your repo
                git branch: 'staging', url: 'https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git'
            }
        }

        // stage('Realease Flask PORT') {
        //     steps {
        //         sh '''
        //             lsof -ti:5005 | xargs kill -9
        //         '''
        //     }
        // }

        stage('Set up Python venv') {
            steps {
                sh '''
                    python3 -m venv flask-firebase-app
                    . flask-firebase-app/bin/activate
                    pip install -r requirements.txt
                    pip install --upgrade pip setuptools
                '''
            }
        }

        
        stage('Run Tests') {
            steps {
                sh '''
                    . flask-firebase-app/bin/activate
                    pytest --maxfail=1 --disable-warnings -q tests/test_app.py
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                    . flask-firebase-app/bin/activate
                    nohup python app.py &

                '''
            }
        }
    }

    post {
    always {
        echo 'Pipeline finished!'
    }
    success {
        mail to: 'harsh24314@gmail.com',
            subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: "Good news! The build succeeded.\nCheck details at: ${env.BUILD_URL}"
        // slackSend(color: 'good', message: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' succeeded.")
    }
    failure {
        mail to: 'harsh24314@gmail.com',
            subject: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: "Unfortunately, the build failed.\nCheck details at: ${env.BUILD_URL}"
        // slackSend(color: 'danger', message: "FAILURE: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' failed.")
    }
}
}