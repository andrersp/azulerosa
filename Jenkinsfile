pipeline {
    agent none
    
    stages {
        stage('build and push web') {
            agent any
            steps {
                script {
                    docker.withRegistry('https://registry.digitalocean.com', 'docker_credentials') {
                        def customImage = docker.build("rspregistry/azulerosa:${BUILD_NUMBER}", "-f Api/Dockerfile .")
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

