pipeline {
    agent {
        docker {
            image 'public.ecr.aws/sam/build-python3.13'
            args '-u root'
        }
    }

    environment {
        AWS_REGION = 'ap-south-1'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install AWS SAM CLI') {
            steps {
                sh '''
                sam --version
                '''
            }
        }

        stage('Determine Environment') {
            steps {
                script {
                    // Determine environment based on branch name
                    def branch = env.BRANCH_NAME
                    if (branch == 'dev') {
                        env.STACK_NAME = 'product-service-dev'
                        env.DEPLOY_ENV = 'dev'
                        env.AWS_CREDENTIALS_ID = 'AWS_DEV'
                    } else if (branch == 'uat') {
                        env.STACK_NAME = 'product-service-uat'
                        env.DEPLOY_ENV = 'uat'
                        env.AWS_CREDENTIALS_ID = 'AWS_UAT'
                    } else if (branch == 'prod') {
                        env.STACK_NAME = 'product-service-prod'
                        env.DEPLOY_ENV = 'prod'
                        env.AWS_CREDENTIALS_ID = 'AWS_PROD'
                    } else {
                        error "Branch ${branch} is not configured for deployment"
                    }
                    
                    echo "Deploying to environment: ${env.DEPLOY_ENV}"
                    echo "Using stack name: ${env.STACK_NAME}"
                }
            }
        }

        stage('Create Environment File') {
            steps {
                script {
                    // Create .env file from existing Jenkins credentials
                    withCredentials([string(credentialsId: env.AWS_CREDENTIALS_ID, variable: 'ENV_CONTENT')]) {
                        writeFile file: '.env', text: "${ENV_CONTENT}"
                    }
                }
            }
        }

        stage('Build SAM Application') {
            steps {
                sh """
                sam build --parameter-overrides Environment=${env.DEPLOY_ENV}
                """
            }
        }

        stage('Deploy to AWS') {
            steps {
                withAWS(credentials: env.AWS_CREDENTIALS_ID, region: "${AWS_REGION}") {
                    sh """
                    sam deploy --stack-name ${env.STACK_NAME} --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset --parameter-overrides Environment=${env.DEPLOY_ENV}
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Deployment to ${env.DEPLOY_ENV} environment failed!"
        }
        success {
            echo "Deployment to ${env.DEPLOY_ENV} environment successful!"
        }
        always {
            cleanWs()
        }
    }
}