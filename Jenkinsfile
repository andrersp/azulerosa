pipeline {
    agent any

    // stages {
    //     stage('build and push web') {
    //         steps {
    //             script {
    //                 docker.withRegistry('', 'docker_credentials') {
    //                     def customImage = docker.build("protesto:${BUILD_NUMBER}", "-f Api/Dockerfile .")

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
    }
}

