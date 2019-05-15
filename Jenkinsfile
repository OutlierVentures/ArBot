node {
    stage "Build"
        checkout scm
        docker.image('ubuntu').inside {
            stage "Install"
                //sh "./install.sh"
            stage "Test"
                //sh "pytest -m 'not needschain'"
        }
}