pipeline {
    agent any

    environment {
        // This pulls your Access Key and Secret Key from the 'aws-creds' ID you created
        AWS_CREDS = credentials('aws-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the latest code from your GitHub repo
                checkout scm
            }
        }

        stage('Terraform Init') {
            steps {
                // Moving into the 'terraform' folder before running init
                dir('terraform') {
                    sh 'terraform init -no-color'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    // Saves the plan to a file so 'Apply' uses the exact same changes
                    sh 'terraform plan -out=tfplan -no-color'
                }
            }
        }

        stage('Manual Approval') {
            steps {
                // This pauses the pipeline so you can verify the plan in the logs
                input message: "Review the plan in logs. Do you want to proceed with the AWS deployment?", ok: "Apply Changes"
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('terraform') {
                    // Uses the plan file created in the previous stage
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }
    }

    post {
        always {
            // Clean up the temporary plan file to keep the workspace tidy
            dir('terraform') {
                sh 'rm -f tfplan'
            }
        }
        success {
            echo "SUCCESS: Your EKS Cluster has been updated/created!"
        }
        failure {
            echo "FAILURE: The pipeline failed. Please check the 'Terraform Plan' logs above."
        }
    }
}
