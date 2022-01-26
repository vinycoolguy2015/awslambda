sed -i "s/ENVIRONMENT/${ENVIRONMENT}/g" /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
systemctl start amazon-cloudwatch-agent
systemctl enable amazon-cloudwatch-agent
