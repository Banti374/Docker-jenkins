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
                  docker save pyapp -o pyapp.tar
                '''
            }
        }

        stage('Deploy Stage') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                sh '''
                  docker load -i pyapp.tar
                  docker run -d --name pythoncontainer -p 80:8080 pyapp || true

                  echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                  docker tag pyapp $DOCKER_USER/pyapp
                  docker push $DOCKER_USER/pyapp
                '''
            }
        }
    }
}

