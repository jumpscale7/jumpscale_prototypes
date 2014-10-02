#Certificate sample

##Generate certificates

Execute `python sslsign.py`, it will generate the following files in `/tmp/keys`:
```
ca.crt
ca.key
client1.example.com.p12
server.crt
server.key
```
The `ca.crt` and `ca.key` files are a self signed certification authority certificate and the corresponding private key.

`server.crt` and `server.key` are a certificate and corresponding private key that can be used in a webserver for SSL (https).
The `server.crt` certificate is signed with the self signed certification authority certificate and key.
Don't do this on production environments.

`client1.example.com.p12` is a pkcs12 bundle containing a private key, a certificate with cn=client1.example.com and the certification authority certificate ca.crt that was used to sign the certificate in this bundle.
The passphrase for this file is "test".

##Run the sample
Install the client1.example.com.p12 as a certificate in your browser.

Enable the nginx site for this demo:
```
sudo ln -s /opt/code/github/jumpscale/jumpscale_prototypes/prototypes/sslsign/nginx_example.conf /etc/nginx/sites-enabled/sslsign
```

And restart nginx
```
sudo service nginx restart
```

Browse to `https://localhost/index.html` if on localhost. Trust the server certifcate, by default it will not be trusted as it is signed by a self signed certification authority certificate/key.
