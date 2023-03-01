FROM hashicorp/terraform:1.0.0 AS terraform

FROM alpine:latest

ARG KUBECTL_VERSION=1.17.5
ENV TF_IN_AUTOMATION true

COPY --from=terraform /bin/terraform /bin
COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod 755 /usr/local/bin/docker-entrypoint.sh && \
    apk add --update --no-cache nodejs npm python3 git curl make gcc g++ openssl-dev && \
    curl -sLO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    mv kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    pip3 install awscli && \
    pip3 cache purge && \
    authenticator=$(aws --no-sign-request s3 ls s3://amazon-eks --recursive |grep aws-iam-authenticator$|grep amd64 |awk '{print $NF}' |sort -V|tail -1) && \
    aws --no-sign-request s3 cp s3://amazon-eks/${authenticator} /usr/bin/aws-iam-authenticator && \
    chmod +x /usr/bin/aws-iam-authenticator

RUN apk --no-cache add ca-certificates && \
wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://raw.githubusercontent.com/sgerrand/alpine-pkg-git-crypt/master/sgerrand.rsa.pub && \
wget https://github.com/sgerrand/alpine-pkg-git-crypt/releases/download/0.6.0-r1/git-crypt-0.6.0-r1.apk && \
apk add git-crypt-0.6.0-r1.apk

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["/bin/terraform"]
