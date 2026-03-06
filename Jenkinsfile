pipeline {
    agent any

    environment {
        // This pulls the Access Key and Secret Key from your 'aws-creds' store
        AWS_ACCESS_KEY_ID     = credentials('aws-creds')
        AWS_SECRET_ACCESS_KEY = credentials('aws-creds')
        AWS_DEFAULT_REGION    = 'us-east-1' 
        TF_IN_AUTOMATION      = 'true'
    }

    stages {
        stage('Checkout') {
            steps {
                // This pulls your latest code from GitHub
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                sh 'terraform init -no-color'
            }
        }

        stage('Terraform Plan') {
            steps {
                // Generates a plan file and saves it so 'Apply' uses the exact same changes
                sh 'terraform plan -out=tfplan -no-color'
            }
        }

        stage('Manual Approval') {
            steps {
                // This pauses the pipeline and waits for you to click "Proceed" in Jenkins
                input message: "Do you want to apply the changes to AWS?", ok: "Proceed"
            }
        }

        stage('Terraform Apply') {
            steps {
                // Uses the plan file from the previous stage
                sh 'terraform apply -auto-approve tfplan'
            }
        }
    }

    post {
        always {
            // Clean up the plan file after the build
            sh 'rm -f tfplan'
        }
        success {
            echo "Infrastructure successfully updated!"
        }
        failure {
            echo "Pipeline failed. Check the logs for errors."
        }
    }
}
