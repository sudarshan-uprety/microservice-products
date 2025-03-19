pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh """#!/bin/bash
                        source ${env.SERVERLESS_VENV}/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }
        
        stage('Install Serverless Plugins') {
            steps {
                script {
                    // Install the necessary Serverless plugins
                    def plugins = [
                        "serverless-deployment-bucket",
                        "serverless-python-requirements",
                        "serverless-dotenv-plugin",
                        "serverless-prune-plugin"
                    ]
                    plugins.each { plugin ->
                        sh "sls plugin install --name ${plugin}"
                    }
                }
            }
        }  

        stage('Prepare Environment File') {
            steps {
                script {
                    // Determine which environment file to use based on branch
                    def branch = env.BRANCH_NAME
                    def envName = "AWS_" + branch.toUpperCase()

                    // Use the dynamically generated environment variable to get the credentials 
                    withCredentials([file(credentialsId: "${envName}", variable: 'ENV_FILE')]) {
                        // Write the content to the .env file
                        writeFile file: '.env', text: readFile(ENV_FILE)
                        sh """
                        serverless deploy --stage ${branch}
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                commiterEmail = sh(script: "git show -s --format='%ae'", returnStdout: true).trim()
            }
            cleanWs()
        }
        failure {
            emailext body: '${DEFAULT_CONTENT}',
                to: commiterEmail, 
                subject: '${DEFAULT_SUBJECT}', 
                saveOutput: false
        }
    }
}