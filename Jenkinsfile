pipeline{
    agent any
    // agent {
    //     docker {
    //         image 'flask-firebase-python-venv-img'
    //         args '-u root'  // ensures root user inside container
    //     }
    // }

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
    
    stages{
        stage('Checkout Code'){
            steps{
                git branch: 'main', url: 'https://github.com/Harshwerdhan/simple-flask-firebase-jenkins-pipeline.git'
            }
        }

        stage("Install dependancies"){
            steps{
                sh 'python3 -m venv flask-firebase-app'
                sh 'source flask-firebase-app/bin/activate'
                sh 'pip install --upgrade pip setuptools'
                sh 'pip install -r requirments.txt'
            }
        }

        stage("Run Test using pytest"){
            steps{
                dir('tests'){
                    sh 'pytest test_app.py'
                }
            }
        }

        stage("Deploy Python App"){
            steps{
                echo "Application is Ready to Go"
            }
        }
    }
}