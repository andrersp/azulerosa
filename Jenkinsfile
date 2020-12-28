pipeline {
    agent any

    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            steps {
                echo "${BUILD_NUMBER}"
            }

        }

    }
}