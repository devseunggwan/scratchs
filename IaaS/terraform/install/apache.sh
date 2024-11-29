# apache http server installation
sudo yum install httpd -y

# apache http server start & 시스템 재부탕 후 자동 apache server 시작
sudo apachectl start
sudo systemctl enable httpd

sudo apachectl configtest

sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --reload