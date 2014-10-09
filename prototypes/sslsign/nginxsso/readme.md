#Single sign on for operator applications

##Concept
The client authenticates itself using a client certificate at the proxy.
The proxy authenticates at the proxied applications and allows the client access to them without being challenged for credentials for those applications.

Since some applications do not behave well when being proxied at specific locations eg. example.com/application/ the choice has been made to proxy them at different domains eg. application.example.com


##Installation
This solution is based on nginx and lua. The easiest way is to use openresty (nginx with lua package).
Use the openresty jpackage.


##Test

Generate and install the necessary certificates as explained in the sslsign readme.

Start nginx on this location and with the proper configuration file:
```
nginx -p `pwd`/ -c conf/nginx.conf
```


Put the following entries in your `/etc/hosts` file and point them to the ip of your nginx installation:

```
www.operator.mothership1.com
racktables.operator.mothership1.com
cbgrid.operator.mothership1.com
icinga.operator.mothership1.com
```

Browse to `www.operator.mothership1.com`
