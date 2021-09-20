#!/bin/sh

REGION="us-east-1"
SERVICE_NAME="springbootapp"
SERVICE_TAG="v1"
AWS_ACCOUNT_ID=xxx
ECR_REPO_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${SERVICE_NAME}"

if [ "$1" = "build" ];then
    cd ..
    sh mvn clean install
elif [ "$1" = "test" ];then
    echo $SERVICE_NAME
    find ../target/ -type f \( -name "*.jar" -not -name "*sources.jar" \) -exec cp {} ../infrastructure/$SERVICE_NAME.jar \;
elif [ "$1" = "dockerize" ];then
    find ../target/ -type f \( -name "*.jar" -not -name "*sources.jar" \) -exec cp {} ../infrastructure/$SERVICE_NAME.jar \;
    aws ecr create-repository --repository-name ${SERVICE_NAME:?} --region ${REGION} || true
    aws ecr get-login-password \
    --region ${REGION} \
    | docker login \
    --username AWS \
    --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

    docker build -t ${SERVICE_NAME}:${SERVICE_TAG} .
    docker tag ${SERVICE_NAME}:${SERVICE_TAG} ${ECR_REPO_URL}:${SERVICE_TAG}
    docker push ${ECR_REPO_URL}:${SERVICE_TAG}
elif [ "$1" = "plan" ];then
    cd infrastructure
    terraform init -backend-config="app-prod.config"
    terraform plan -var "docker_image_url=$ECR_REPO_URL:$SERVICE_TAG"
elif [ "$1" = "deploy" ];then
    terraform init -backend-config="app-prod.config"
    terraform apply -var "docker_image_url=$ECR_REPO_URL:$SERVICE_TAG" -auto-approve
elif [ "$1" = "destroy" ];then
    cd infrastructure
    terraform init -backend-config="app-prod.config"
    terraform destroy -var "docker_image_url=$ECR_REPO_URL:$SERVICE_TAG" -auto-approve
fi
