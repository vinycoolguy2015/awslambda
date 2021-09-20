brew install java
brew install maven
M2_HOME=/usr/local/Cellar/maven/3.8.2
export M2_HOME

cd infrastructure
./deploy.sh build
./deploy.sh dockerize # Change tag from v1 to subsequent
./deploy.sh deploy
./deploy.sh destroy
