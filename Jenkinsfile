pipeline {
    agent {
    kubernetes {
      	cloud 'kubernetes'
      	defaultContainer 'jnlp'
      }
    }

    stages {

        stage("Echo") {
            steps {
                echo "Andre Luis"
            }
        }


        stage('deploy k8s') {
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kubeconfig")
                }
            }
        }
    }
}