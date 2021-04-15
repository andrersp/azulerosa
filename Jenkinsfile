pipeline {
    agent {
    kubernetes {
      	cloud 'kubernetes'
      	defaultContainer 'jnlp'
      }
    }

    stages {

        stages {
        stage('build and push web') {
            steps {
                script {
                    docker.withRegistry('https://dh.inquest.tech', 'docker_credentials') {
                        def customImage = docker.build("protesto:${BUILD_NUMBER}", "-f dockerfiles/Dockerfile .")

                        /* Push the container to the custom Registry */
                        customImage.push()
                    }
                }
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