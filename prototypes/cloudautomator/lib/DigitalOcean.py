from dop.client import Client
from JumpScale import j

import time
from SSH import SSH


class Base():

    def __init__(self, ddict, client):
        self.__dict__ = ddict.to_json()
        self.client = client

    def __repr__(self):
        return str(self.__dict__)

    __str__ = __repr__


class Droplet(Base):

    """
    example
    {'backups_active': None,
     'event_id': -1,
     'id': 242025,
     'image_id': 456928,
     'ip_address': u'37.139.2.74',
     'name': u'test2',
     'region_id': 2,
     'size_id': 66,
     'status': u'active'}
    """

    def delete(self):
        self.client.destroy_droplet(self.id)

    def halt(self):
        result = self.client.power_off_droplet(self.id)

    def start(self):
        result = self.client.power_on_droplet(self.id)

    def checkStatus(self):
        return str(self.client.show_droplet(self.id).status.lower().strip())

    def waitOff(self, timeout=90):
        start = j.base.time.getTimeEpoch()
        now = start
        while now < start + timeout:
            if self.checkStatus() == "off":
                return "OK"
            time.sleep(1)
            print "waiting for off for %s" % self.name
            now = j.base.time.getTimeEpoch()
        j.errorconditionhandler.raiseOperationalCritical(msgpub="Could not stop %s" % self.name, category="digitalocean.waitoff")

    def waitStart(self, timeout=90):
        start = j.base.time.getTimeEpoch()
        now = start
        while now < start + timeout:
            ##TODO

            if self.checkStatus() == "off":
                return "OK"
            time.sleep(1)
            print "waiting for off for %s" % self.name
            now = j.base.time.getTimeEpoch()
        j.errorconditionhandler.raiseOperationalCritical(msgpub="Could not stop %s" % self.name)

    def snapshot(self):
        ##TODO
        pass

    def changeRootPasswd(self, newPasswd):
        ssh = SSH(self.ip_address)
        ssh.changePasswd(newPasswd)


class Region(Base):

    """
    """


class Image(Base):

    """
    """


class Size(Base):

    """
    """


class DigitalOcean():

    def __init__(self):
        self.client = Client('PUPdwX4Dwbl9Xc3lYrhEp', 'vYe2LKXyP1Dfa3lKX6ASg2vEhd6xJFt0HXpfE500n')
        self.images = []
        self.sizes = []
        self.regions = []
        self.refresh = True

    def getRegions(self):
        if self.refresh or self.regions == []:
            self.regions = []
            self.regions = [Region(item, self.client) for item in self.client.regions()]
        return self.regions

    def getDroplets(self, prefix="", refresh=False):
        if refresh or self.refresh or self.droplets == []:
            self.droplets = []
            droplets = self.client.show_active_droplets()
            for item in droplets:
                self.droplets.append(Droplet(item, self.client))

        if prefix != "":
            result = []
            for item in self.droplets:
                nname = str(item.name).strip()
                if nname.find(prefix) == 0:
                    result.append(item)
            return result
        else:
            return self.droplets

    def getImages(self):
        if self.refresh or self.images == []:
            self.images = []
            self.images = [Image(item, self.client) for item in self.client.images()]
            self.images += [Image(item, self.client) for item in self.client.images(show_all=False)]
        return self.images

    def getSizes(self):
        if self.refresh or self.sizes == []:
            self.sizes = [Size(item, self.client) for item in self.client.sizes()]
        return self.sizes

    def getALL(self):
        self.getSizes()
        self.getImages()
        self.getDroplets()
        self.getRegions()

    def getImageFromName(self, name):
        images = self.getImages()
        for item in images:
            if item.name.find(name) != -1:
                return item
        return None

    def getImage(self, name):
        items = self.getImages()
        for item in items:
            if item.name.find(name) != -1:
                return item
        return None

    def getDroplet(self, name, refresh=False):
        items = self.getDroplets(refresh=refresh)
        for item in items:
            if item.name.find(name) == 0:
                return item
        return None

    def deleteDroplets(self, prefix):
        self.haltDroplets(prefix)
        for droplet in self.getDroplets(prefix):
            droplet.waitOff()
        for droplet in self.getDroplets(prefix):
            droplet.delete()
        if self.getDroplets(prefix) == []:
            return
        print "wait till all deleted"
        time.sleep(5)
        start = j.base.time.getTimeEpoch()
        now = start
        timeout = 60
        while now < start + timeout:
            droplets = self.getDroplets(prefix, refresh=True)
            if droplets == []:
                return
            time.sleep(1)
            print "wait till all deleted"
            now = j.base.time.getTimeEpoch()
        j.errorconditionhandler.raiseOperationalCritical(msgpub="Could not delete droplets with prefix %s" % self.prefix)

    def haltDroplets(self, prefix):
        for droplet in self.getDroplets(prefix):
            droplet.halt()

    def startDroplets(self, prefix):
        for droplet in self.getDroplets(prefix):
            droplet.start()

    def save(self, name="main"):
        items = {}
        items["images"] = self.images
        items["sizes"] = self.sizes
        items["regions"] = self.regions
        items["refresh"] = self.refresh

        txt = j.db.serializers.ujson.dumps(items)
        j.system.fs.writeFile("%s.json" % name, txt)

    def load(self, name="main"):
        txt = j.system.fs.fileGetContents("%s.json" % name)
        self.__dict__.update(j.db.serializers.ujson.loads(txt))

    def getMainSSHKey(self):
        key = self.client.all_ssh_keys()[0]
        return key.id

    def createMachine(self, name, size=66, image=350076, region=2, sshkey=0):
        """
        regions : 2=amsterdam
        """
        self.client.create_droplet(name=name, size_id=size, image_id=image, region_id=region, ssh_key_ids=sshkey, virtio=True)

    def changeRootPasswd(self, prefix, newPasswd):
        droplets = self.getDroplets(prefix)
        for droplet in droplets:
            droplet.changeRootPasswd(newPasswd)

    def createMachines(self, nr, prefix, size=66, image=350076, region=2, sshkey=0, rootPasswd=""):
        print "create machines with prefix: %s" % prefix
        names = []
        for i in range(nr):
            name = "%s-%s" % (prefix, i)
            names.append(name)
            self.createMachine(name, size, image, region, sshkey)

        print "wait till all created"
        start = j.base.time.getTimeEpoch()
        now = start
        timeout = 600
        time.sleep(40)
        while now < start + timeout:
            self.getDroplets(refresh=True)  # makes sure we read all machines again
            for name in names:
                dr = self.getDroplet(name)
                if dr.checkStatus() == "active":
                    names.remove(name)
            if names == []:
                break
            time.sleep(10)
            print "wait"
            now = j.base.time.getTimeEpoch()

        if name != []:
            j.errorconditionhandler.raiseOperationalCritical(msgpub="Could not create droplets %s" % names, category="digitalocean.create")

        self.droplets = []

        if rootPasswd != "":
            self.changeRootPasswd(prefix, rootPasswd)
