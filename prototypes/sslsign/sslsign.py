from JumpScale import j
from OpenSSL import crypto, SSL
import OpenSSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join





def create_self_signed_ca_cert(cert_dir):
    """
    is for CA
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """

    CERT_FILE = "ca.crt"
    KEY_FILE = "ca.key"

    if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # create a self-signed cert
        cert = crypto.X509()
        cert.set_version(3)
        cert.get_subject().C = "US"
        cert.get_subject().ST = "Minnesota"
        cert.get_subject().L = "Minnetonka"
        cert.get_subject().O = "my company"
        cert.get_subject().OU = "my organization"
        cert.get_subject().CN = gethostname()

        import time
        cert.set_serial_number(int(time.time() * 1000000))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)

        cert.add_extensions([
          OpenSSL.crypto.X509Extension("basicConstraints", True,
                                       "CA:TRUE, pathlen:0"),
          OpenSSL.crypto.X509Extension("keyUsage", True,
                                       "keyCertSign, cRLSign"),
          OpenSSL.crypto.X509Extension("subjectKeyIdentifier", False, "hash",
                                       subject=cert),
          ])

        cert.sign(k, 'sha1')

        open(join(cert_dir, CERT_FILE), "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


def createSignedCert(path, keyname):
    """
    Signing X509 certificate using CA
    The following code sample shows how to sign an X509 certificate using a CA:
    """
    cacert=j.system.fs.fileGetContents("%s/ca.crt"%path)
    cakey=j.system.fs.fileGetContents("%s/ca.key"%path)
    ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,cacert)
    ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,cakey)

    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    cert = OpenSSL.crypto.X509()
    cert.get_subject().CN = "node1.example.com"
    import time
    cert.set_serial_number(int(time.time() * 1000000))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(24 * 60 * 60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(ca_key, "sha1")

    with open(join(path, "%s.crt"%keyname), "wt") as cfile:
        cfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(join(path, "%s.key"%keyname), "wt") as kfile:
        kfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

def createCertificateSigningRequest(common_name):
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    req = OpenSSL.crypto.X509Req()
    req.get_subject().commonName = common_name

    req.set_pubkey(key)
    req.sign(key, "sha1")

    # Write private key
    key=OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)

    # Write request
    req= OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)
    return key,req

def signRequest(req, ca_cert, ca_key):

    req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM,req)

    cert = OpenSSL.crypto.X509()
    cert.set_subject(req.get_subject())
    import time
    cert.set_serial_number(int(time.time() * 1000000))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(24 * 60 * 60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(ca_key, "sha1")

    pubkey= OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    return pubkey

def verify(path):
    #Verify whether X509 certificate matches private key
    #The code sample below shows how to check whether a certificate matches with a certain private key.
    #OpenSSL has a function for this, X509_check_private_key, but pyOpenSSL provides no access to it.

    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
    ctx.use_privatekey(key)
    ctx.use_certificate(cert)
    try:
      ctx.check_privatekey()
    except OpenSSL.SSL.Error:
      print "Incorrect key"
    else:
      print "Key matches certificate"

def bundle(certificate, key, certification_chain=(), passphrase=None):
    """
    Bundles a certificate with it's private key (if any) and it's chain of trust.
    Optionally secures it with a passphrase.
    """
    key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,key)

    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)

    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(x509)
    p12.set_ca_certificates(certification_chain)
    p12.set_friendlyname('Jumpscale client authentication')
    return p12.export(passphrase=passphrase)



path="/tmp/keys"

cacrt_filename = "%s/ca.crt"%path
cakey_filename = "%s/ca.key"%path

j.system.fs.removeDirTree(path)
j.system.fs.createDir(path)
create_self_signed_ca_cert(path)

cacert_filecontent=j.system.fs.fileGetContents(cacrt_filename)
cakey_filecontent=j.system.fs.fileGetContents(cakey_filename)
ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,cacert_filecontent)
ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,cakey_filecontent)

createSignedCert(path, "server")
prikey,req=createCertificateSigningRequest("client1.example.com")
clientcert=signRequest(req, ca_cert, ca_key)

clientcert_package = bundle(clientcert, prikey, [ca_cert], "test")

with open("%s/client1.example.com.p12"%path,"w") as cfile:
    cfile.write(clientcert_package)



#import ipdb; ipdb.set_trace()
