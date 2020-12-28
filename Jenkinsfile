pipeline {
    agent any

    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            steps {
                sh "docker-compose build"
                sh "docker-compose up -d"           
            }

        }

    }
}