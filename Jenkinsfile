pipeline {
  agent {
    kubernetes {
      yaml """\
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            some-label: some-label-value
        spec:
          containers:
          - name: slave
            image: rspandre/jenkins-slave:1          
          
          
        """.stripIndent()
    }
  }
  stages {
    stage('deploy k8s') {
            
            steps {
                script {
                    kubernetesDeploy(configs: "manifest-dev.yaml", kubeconfigId: "kubeconfig")
                }
            }
        }
  }
}