pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kube-config")
                }          
            }

        }

    }
}