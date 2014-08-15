from JumpScale import j

j.application.start("tempinstaller")

import time

from JumpScale.baselib.installtools.InstallTools import InstallTools


class HadoopInstaller(InstallTools):

    def installJava(self):
        qp = j.qp.find("java*")[0]
        qp.install()
        # result=self.execute("java -version")

        # if result.find("java version")<>-1:
        # @todo will need to be more specific about which java version
        # 	return

        # cmd="apt-get install openjdk-6-jre-headless"
        # self.execute(cmd)

    def installElasticSearch(self):

        path = "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.1.deb"
        debpath = installer.getTmpPath("hadoop.deb")
        self.download(path, debpath)

        cmd = "cd /tmp;export JAVA_HOME=/opt/jdk1.7;dpkg -i %s" % debpath
        self.execute(cmd)

    def downloadInstallHadoop(self):
        self.installJava()
        hadoopsource = "http://apache.cu.be/hadoop/common/hadoop-1.1.2/hadoop_1.1.2-1_i386.deb"
        debpath = installer.getTmpPath("hadoop.deb")
        # installer.download(hadoopsource,debpath)
        cmd = "cd %s;export JAVA_HOME=/opt/jdk1.7;dpkg -i hadoop.deb" % (self.TMP)
        self.execute(cmd)
        print "set etc/hadoop/hadoop-env.sh export JAVA_HOME=/opt/apps/jdk1.7"  # @todo create qpackage make all clean

installer = HadoopInstaller()
installer.downloadInstallHadoop()

j.application.stop()
