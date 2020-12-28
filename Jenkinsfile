pipeline {
    agent any

    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            steps {
                docker-compose up -d --build
                docker-compose exec api python app.py create_db
            }

        }

    }
}