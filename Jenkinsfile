pipeline {
    agent none
    
    stages {
        stage('build and push web') {
            agent any
            steps {
                script {
                    docker.withRegistry('', 'docker_credentials') {
                        def customImage = docker.build("protesto:${BUILD_NUMBER}", "-f dockerfiles/Dockerfile .")

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

