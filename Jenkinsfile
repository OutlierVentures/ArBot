pipeline {

    agent {
        docker {
            image "ubuntu:latest"
        }
    }

    stages {
        
        stage('Install') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y build-essential git curl python3 python3-pip
                    curl -fsSL https://get.docker.com -o get-docker.sh
                    sh get-docker.sh
                    curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    chmod +x /usr/local/bin/docker-compose
                    pip3 install setuptools pytest
                '''
                sh "pip3 install ."
            }
        }

        stage('Build') {
            steps {
                sh "cd nodes && ./get_nodes.sh"
                sh "cd nodes && ./start_nodes.sh"
            }
        }

        stage('Test') {
            steps {
                sh "pytest"
                sh "cd nodes && ./stop_nodes.sh"
            }  
        }
    
    }

}