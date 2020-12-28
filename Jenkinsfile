pipeline {
    agent any

    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            steps {
                sh "docker-compose up -d --build"
                sh "docker-compose exec api python app.py create_db"
            }

        }

    }
}