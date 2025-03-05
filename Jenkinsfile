pipeline {
    agent any

    environment {
        // AWS Credentials
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_KEY')
        
        // Environment-specific env files
        DEV_ENV = credentials('AWS_DEV')
        UAT_ENV = credentials('AWS_UAT')
        PROD_ENV = credentials('AWS_PROD')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    // Install Python dependencies
                    sh 'pip3 install -r requirements.txt'
                }
            }
        }
        
        stage('Prepare Environment File') {
            steps {
                script {
                    // Determine which environment file to use based on branch
                    if (env.BRANCH_NAME == 'dev') {
                        writeFile file: '.env', text: env.DEV_ENV
                    } else if (env.BRANCH_NAME == 'uat') {
                        writeFile file: '.env', text: env.UAT_ENV
                    } else if (env.BRANCH_NAME == 'prod') {
                        writeFile file: '.env', text: env.PROD_ENV
                    } else {
                        error "No environment file for branch: ${env.BRANCH_NAME}"
                    }
                }
            }
        }
        
        stage('Serverless Doctor') {
            steps {
                sh 'serverless doctor'
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Deploy based on branch
                    switch(env.BRANCH_NAME) {
                        case 'dev':
                            sh 'serverless deploy --stage dev'
                            break
                        case 'uat':
                            sh 'serverless deploy --stage uat'
                            break
                        case 'prod':
                            sh 'serverless deploy --stage prod'
                            break
                        default:
                            echo "Skipping deployment for branch: ${env.BRANCH_NAME}"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        
        success {
            echo 'Deployment completed successfully!'
        }
        
        failure {
            echo 'Deployment failed. Please check the logs.'
        }
    }
}