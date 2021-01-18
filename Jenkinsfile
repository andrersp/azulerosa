pipeline {
    agent any


    stage("echos") {
        steps {
            echo "Andre"
        }
    }
    
    stage('deploy k8s') {
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kube-config")
                }
            }
        }
    

    }
}