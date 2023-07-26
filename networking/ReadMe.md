
https://www.baeldung.com/linux/nginx-config-environment-variables

https://flask-security-too.readthedocs.io/en/stable/spa.html#nginx

# dev nginx and certbot

https://www.tecmint.com/setup-https-with-lets-encrypt-ssl-certificate-for-nginx-on-centos/

## commands to install nginx and install certbot

    sudo yum install nginx
    sudo systemctl status nginx
    sudo systemctl start nginx
    visit http://xxx.xxx.xx.xxx/

    sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
    sudo dnf install python3-certbot-nginx

    sudo certbot --nginx -d dev1.dmtool.info
    
## output from above
    
    Requesting a certificate for dev1.dmtool.info
    
    Successfully received certificate.
    Certificate is saved at: /etc/letsencrypt/live/dev1.dmtool.info/fullchain.pem
    Key is saved at:         /etc/letsencrypt/live/dev1.dmtool.info/privkey.pem
    This certificate expires on 2023-10-24.
    These files will be updated when the certificate renews.
    Certbot has set up a scheduled task to automatically renew this certificate in the background.
    
    Deploying certificate
    Successfully deployed certificate for dev1.dmtool.info to /etc/nginx/nginx.conf
    Congratulations! You have successfully enabled HTTPS on https://dev1.dmtool.info
    
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    If you like Certbot, please consider supporting our work by:
     * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
     * Donating to EFF:                    https://eff.org/donate-le
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
