pipeline {
    agent any

    environment {
        // This pulls your Access Key and Secret Key from the 'aws-creds' store
        AWS_CREDS = credentials('aws-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                // No 'dir' block needed because files are in the root
                sh 'terraform init -upgrade -no-color'
            }
        }

        stage('Terraform Plan') {
            steps {
                sh 'terraform plan -out=tfplan -no-color'
            }
        }

        stage('Manual Approval') {
            steps {
                input message: "Review the plan. Do you want to proceed?", ok: "Apply Changes"
            }
        }

        stage('Terraform Apply') {
            steps {
                sh 'terraform apply -auto-approve tfplan'
            }
        }
    }

    post {
        always {
            sh 'rm -f tfplan'
        }
        success {
            echo "SUCCESS: Infrastructure is live!"
        }
        failure {
            echo "FAILURE: Check the logs above."
        }
    }
}
