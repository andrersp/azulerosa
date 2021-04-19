pipeline {
    agent none
    
    stages {
        stage('build and push web') {
            agent docker
            steps {
                script {
                    docker.withRegistry('registry.digitalocean.com/rspregistry', 'docker_credentials') {
                        def customImage = docker.build("azulerosa:${BUILD_NUMBER}", "-f Api/Dockerfile .")

                        /* Push the container to the custom Registry */
                        customImage.push()
                    }
                }
            }
        }        
        
        stage('deploy k8s') {
            agent {
                kubernetes {
                    cloud 'kubernetes'
                    defaultContainer 'jnlp'
                }
                }
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kubeconfig")
                }
            }
        }
    }
}

