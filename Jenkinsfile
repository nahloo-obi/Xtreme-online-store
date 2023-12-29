pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerID')
        AWS_CREDENTIALS = credentials('awsID')
        ELASTIC_BEANSTALK_ENV_NAME = credentials('elasticbeanstalkID')
        DB_PASSWORD_CREDENTIALS = credentials('db-password-credentials-id')
    }

    stages {
        stage('Checkout Git Repository') {
            steps {
                checkout scm
            }
        }

        stage('Create .env File') {
            steps {
                script {
                    // Retrieve credentials
                    def dbPassword = credentials('db-password-credentials-id').toString()
                    def dbName = credentials('db-name-credentials-id').toString()
                    def dbUser = credentials('db-user-credentials-id').toString()
                    def dbPort = credentials('db-port-credentials-id').toString()
                    def secret_key = credentials('secret-key-id').toString()
                    def paypal_client_id = credentials('paypal-client-id').toString()
                    def allowed_hosts = credentials('allowed-hosts-id').toString()
                    def debug = credentials('debug-id').toString()
                    def dbhost = credentials('dbhost-id').toString()


                    // Create .env file
                    sh "echo 'DB_NAME=${dbName}' >> .env"
                    sh "echo 'DB_USER=${dbUser}' >> .env"
                    sh "echo 'DB_PASS=${dbPassword}' >> .env"
                    sh "echo 'DB_PORT=${dbPort}' >> .env"
                    sh "echo 'SECRET_KEY=${secret_key}' >> .env"
                    sh "echo 'PAYPAL_CLIENT_ID=${paypal_client_id}' >> .env"
                    sh "echo 'DEBUG=${debug}' >> .env"
                    sh "echo 'ALLOWED_HOSTS=${allowed_hosts}' >> .env"
                    sh "echo 'DB_HOST=${dbhost}' >> .env"

                    // Add other environment variables to .env as needed
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Authenticate with Docker Hub
                    withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerID', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD']]) {
                        sh "docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD"
                    }

                    // Build and push Docker image to Docker Hub
                    sh 'docker-compose build'

                    // Get the current directory name (Jenkins workspace or project name)
                    def currentDirName = sh(script: 'basename $PWD', returnStdout: true).trim()

                    // Tag Docker image with a version or tag (replace 'your-tag' with your desired tag)
                    sh "docker tag ${currentDirName}_app:latest nahlooobi/xtremestoreapp:latest"

                    sh 'docker push nahlooobi/xtremestoreapp:latest'
                }
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                script {
                    // Authenticate with AWS
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY', credentialsId: 'awsID']]) {
                        // Deploy to Elastic Beanstalk
                        sh "eb create ${ELASTIC_BEANSTALK_ENV_NAME}"
                    }
                }
            }
        }

        // Add other stages as needed
    }
}
