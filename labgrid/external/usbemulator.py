import pexpect
import subprocess

HOST = '192.168.24.137'
IMAGE_NAME = 'backing_store'

class USBStick():
    _UNPLUGGED = 1
    _PLUGGED = 2

    def __init__(self):
        self.host = HOST
        self.image_name = IMAGE_NAME
        self.ssh("mount /dev/mmcblk1p1 /mnt")

    def plug_in(self):
        self.ssh("modprobe g_mass_storage file=/mnt/{image}".format(image=self.image_name))

    def eject(self):
        self.ssh("modprobe -r g_mass_storage")

    def upload_file(self, filename):
        subprocess.call('scp {filname} {host}:/tmp/{filename}').format(filename=filename)

    def upload_image(self, image):
        if not self.status == USBStick.UNPLUGGED:
            raise StateException("Device stioll plugged in, can't insert new image")
        subprocess.call('scp {filname} {host}:/tmp/{image}').format(filename=image)

    def ssh(self, cmd):
        try:
            call = subprocess.call('ssh {host} {cmd}').format(host=self.host, cmd=cmd)
        except:
            raise ExecutionException('Call failed: {}'.format(call))

    def __del__(self):
        self.ssh("modprobe -r g_mass_storage")

class ExecutionException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "ExecutionException({msg})".format(msg=self.msg)

class StateException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "StateException({msg})".format(msg=self.msg)
