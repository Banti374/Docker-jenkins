pipeline {
    agent any

    environment {
        // Docker
        IMAGE_NAME     = "bansil374/pyapp"
        CONTAINER_NAME = "pythoncontainer"

        // Prod servers
        PROD_SERVER1 = "13.203.219.118"
        //PROD_SERVER2 = "43.204.116.78"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  docker --version
                  docker build -t pyapp .
                '''
            }
        }

        stage('Docker Login & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'Docker_cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker tag pyapp $IMAGE_NAME
                      docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('Deploy to Prod Servers') {
            steps {
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ec2-key',
                    keyFileVariable: 'SSH_KEY',
                    usernameVariable: 'SSH_USER'
                )]) {
                    sh '''
                      for SERVER in $PROD_SERVER1        '''$PROD_SERVER2'''
                      do
                        echo "Deploying to $SERVER"

                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY $SSH_USER@$SERVER "

                        
                        sudo apt install -y docker.io
                        docker --version

                        
                        sudo systemctl enable docker
                        sudo systemctl start docker
                        sudo systemctl enable docker.service
                        sudo systemctl enable docker.socket
                        sudo systemctl start docker.service
                        sudo usermod -aG docker ubuntu


                          docker pull $IMAGE_NAME
                          docker stop $CONTAINER_NAME || true
                          docker rm -f $CONTAINER_NAME || true
                          docker run -d \
                            --name $CONTAINER_NAME \
                            -p 8081:8081 \
                            $IMAGE_NAME

                        "
                      done
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "-----****--_Deployment successful on all prod servers_--****-----"
        }
        failure {
            echo "-----****--_Deployment failed_--****-----"
        }
    }
}
