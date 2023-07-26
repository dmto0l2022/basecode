
https://www.baeldung.com/linux/nginx-config-environment-variables

https://flask-security-too.readthedocs.io/en/stable/spa.html#nginx

# dev nginx and certbot

https://www.tecmint.com/setup-https-with-lets-encrypt-ssl-certificate-for-nginx-on-centos/

## commands to install nginx and install certbot

    yum install nginx
    sudo systemctl status nginx
    sudo systemctl start nginx
    visit http://xxx.xxx.xx.xxx/
    sudo systemctl stop nginx

    sudo yum install certbot python3-certbot-nginx
