#!/bin/bash

# 
yum update -y

# 
yum install -y docker

# 
systemctl start docker
systemctl enable docker

# ec2-user -> group docker
usermod -aG docker ec2-user

# 
exec > /var/log/userdata.log 2>&1

echo "=== Starting bulls_web container ==="

# 
docker pull rizvashi/bulls_web:latest
docker run -d -p 8080:8080 rizvashi/bulls_web:latest

echo "=== Done ==="
