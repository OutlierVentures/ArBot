pipeline {

  agent none

  stages {

    stage('Test') {
      parallel {

        stage('Python 2.7') {

          agent {
            docker {
              image "python:2.7-alpine"
            }
          }

          steps {
            sh 'pip install pytest'
            //sh "pytest -m 'not needschain'"
          }

        }

        stage('Python 3.6') {

          agent {
            docker {
              image "python:3.6-alpine"
            }
          }

          steps {
            sh 'pip3 install pytest'
            //sh "pytest -m 'not needschain'"
          }

        }

        stage('Python 3.7') {

          agent {
            docker {
              image "python:3.7-alpine"
            }
          }

          steps {
            sh 'pip3 install pytest'
            //sh "pytest -m 'not needschain'"
          }

        }

      }
    }

  }

} 
