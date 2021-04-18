pipeline {
    agent {
                kubernetes {
                    cloud 'kubernetes'
                    defaultContainer 'jnlp'
                }
                }
    
    stages {
    //     stage('build and push web') {
    //         agent: any
            
    //         steps {
    //             script {
    //                 docker.withRegistry('https://dh.inquest.tech', 'docker_credentials') {
    //                     def customImage = docker.build("azulerorosa:${BUILD_NUMBER}", "-f Api/Dockerfile .")

    //                     /* Push the container to the custom Registry */
    //                     customImage.push()
    //                 }
    //             }
    //         }
    //     }        
        
        stage('deploy k8s') {
            
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kubeconfig")
                }
            }
        }

        stage('deploy Secrerts') {
            
            steps {
                script {
                    kubernetesDeploy(configs: "secrets.json", kubeconfigId: "kubeconfig")
                }
            }
        }
    }
}

