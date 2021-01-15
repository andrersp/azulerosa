pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "config_kubernet")
                }          
            }

        }

    }
}