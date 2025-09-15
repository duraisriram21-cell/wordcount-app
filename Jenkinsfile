pipeline {
  agent any
  environment {
    REGION = 'us-east-2'
    REPO   = 'wordcount-app'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Docker Build') {
      steps {
        sh 'docker build -t wordcount-app:latest .'
      }
    }

    stage('ECR Login') {
      steps {
        sh '''
          ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
          aws ecr get-login-password --region ${REGION} \
            | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
        '''
      }
    }

    stage('Tag & Push') {
      steps {
        sh '''
          ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
          IMAGE_URI=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO}:latest

          # Create repo if it doesn’t exist
          aws ecr describe-repositories --repository-names ${REPO} --region ${REGION} \
            || aws ecr create-repository --repository-name ${REPO} --region ${REGION}

          docker tag wordcount-app:latest ${IMAGE_URI}
          docker push ${IMAGE_URI}
          echo "✅ Pushed: ${IMAGE_URI}"
        '''
      }
    }
  }

  post {
    success { echo '✅ Build & push to ECR completed.' }
    failure { echo '❌ Build failed. Check logs.' }
  }
}
