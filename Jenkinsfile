pipeline {
    agent any

    environment {
        IMAGE_NAME = "pyapp"
    }

    stages {

        stage('Build Stage') {
            steps {
                sh '''
                    docker --version
                    docker build -t pyapp .
                '''
            }
        }

        stage('Docker Image Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag pyapp $DOCKER_USER/pyapp
                        docker push $DOCKER_USER/pyapp
                    '''
                }
            }
            
        }

        stage('Deploy Stage') {
            steps {
                    sh '''
                        ssh ubuntu@3.111.35.233 '
                        docker stop myapp || true
                        docker rm -f pythoncontainer || true
                        docker run -d --name pythoncontainer -p 8081:8081 pyapp

                        ssh ubuntu@3.109.155.195 '
                        docker stop myapp || true
                        docker rm -f pythoncontainer || true
                        docker run -d --name pythoncontainer -p 8081:8081 pyapp
                    '''
                }
            
        }
    }
}
