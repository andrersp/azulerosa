pipeline {
      agent {
    kubernetes {
      //cloud 'kubernetes'
      containerTemplate {
        name 'slave'
        image 'rspandre/jenkins-slave:1'
        ttyEnabled true
        command 'cat'
      }
    }
  }
    
    stages {
        stage('build and push web') {
            
            steps {
                script {
                    docker.withRegistry('https://dh.inquest.tech', 'docker_credentials') {
                        def customImage = docker.build("azulerosa:${BUILD_NUMBER}", "-f Api/Dockerfile .")

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

