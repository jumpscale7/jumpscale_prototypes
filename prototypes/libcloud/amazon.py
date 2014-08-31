from JumpScale import j
j.application.start('filerobot')

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

ACCESS_ID = '???'
SECRET_KEY = '???'

IMAGE_ID = 'ami-4cdc043b'  #ubuntu 14.04
SIZE_ID = 't1.micro'
# SIZE_ID = 'm1.medium'

cls = get_driver(Provider.EC2_EU_WEST)
driver = cls(ACCESS_ID, SECRET_KEY)

sizes = driver.list_sizes()
images = driver.list_images()

kdspem="""
-----BEGIN RSA PRIVATE KEY-----
????
-----END RSA PRIVATE KEY-----
"""

mykey= j.system.fs.fileGetContents("/root/.ssh/id_dsa.pub")

# Shell script to run on the remote server
SCRIPT = '''#!/usr/bin/env bash
apt-get -y update && apt-get -y install mc
'''
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment, SSHKeyDeployment
# Note: This key will be added to the authorized keys for the root user
# (/root/.ssh/authorized_keys)
step_1 = SSHKeyDeployment(mykey)

# A simple script to install puppet post boot, can be much more complicated.
step_2 = ScriptDeployment(SCRIPT)

msd = MultiStepDeployment([step_1, step_2])

def ffind():
    size = [s for s in sizes if s.id == SIZE_ID][0]
    for image in images:
        if image.name<>None:
            name=image.name.lower()
            if name.find("ubuntu")<>-1 and name.find("14.04")<>-1:
                print image

image = [i for i in images if i.id == IMAGE_ID][0]
size = [s for s in sizes if s.id == SIZE_ID][0]

#the multideploy is not working
node = driver.create_node(name='test-node2', image=image, size=size,ex_keyname="kds",deploy=msd)

# Here we allocate and associate an elastic IP
elastic_ip = driver.ex_allocate_address()
driver.ex_associate_address_with_node(node, elastic_ip)

# When we are done with our elastic IP, we can disassociate from our
# node, and release it
# driver.ex_disassociate_address(elastic_ip)
# driver.ex_release_address(elastic_ip)

nodes=driver.list_nodes()
node=nodes[0]




from IPython import embed
print "DEBUG NOW ooo"
embed()


print driver.list_sizes()

j.application.stop()