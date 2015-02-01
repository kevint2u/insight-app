#!/usr/bin/env python
import shutil
import urllib2
import platform
import tempfile
import urllib
import os
import subprocess
import webbrowser
import stat

URL = 'https://github.com/kurtisnelson/wearscript-android/releases/download/v0.4.1/'

def browser(url):
    print('Open this url in a browser: ' + url)
    #webbrowser.open(url)

class InstallerLinux(object):

    def __init__(self):
        self.apks = [URL + 'CaptureActivity.apk', URL + 'OpenCV_2.4.6_Manager_2.9_armv7a-neon.apk', URL + 'WearScript-release.apk', URL + 'picarus.apk']
        self.urls = [URL + 'adb.linux']
        self.adb_name = 'adb.linux'
        self.directory = tempfile.mkdtemp()
        self.adb = os.path.join(self.directory, self.adb_name)
        print('Working Directory: ' + self.directory)

    def _screen_on(self):
        if not self._screen_state():
            p = subprocess.Popen([self.adb, 'shell', 'input', 'keyevent', '26'])
            r = p.wait()

    def _screen_state(self):
        p = subprocess.Popen([self.adb, 'shell', 'dumpsys', 'input_method'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return p.communicate()[0].find('mScreenOn=true') != -1

    def download(self):
        for url in self.urls + self.apks:
            print('Downloading: ' + url)
            urllib.urlretrieve(url, os.path.join(self.directory, os.path.basename(url)))

    def chmod_adb(self):
        mode = stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR
        os.chmod(self.adb, mode)

    def connect_glass(self):
        print('Make sure Glass is in debug mode (instructions http://goo.gl/vEoyul) or your Android phone is in developer mode (http://goo.gl/E0hXdj) and connect it...waiting')
        while 1:
            try:
                p = subprocess.Popen([self.adb, 'shell', 'ls'], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            except OSError:
                raise RuntimeError('Cannot execute adb\nYou may have a 64 bit processor and need the 32 bit libs.\nOn Ubuntu try: sudo apt-get install --reinstall libc6-i386 libncurses5:i386 libstdc++6:i386')
            r = p.wait()
            if r == 0:
                print('Glass connected')
                break

    def push_apks(self):
        print('Uninstalling any previous WearScript...')
        try:
            p = subprocess.Popen([self.adb, 'uninstall', 'com.dappervision.wearscript'])
            r = p.wait()
        except:
            pass
        print('Installing APKs...')
        for apk_url in self.apks:
            apk = os.path.join(self.directory, os.path.basename(apk_url))
            p = subprocess.Popen([self.adb, 'install', '-r', apk])
            r = p.wait()

    def authenticate(self):
        url = 'https://api.wearscript.com/'
        browser(url)
        print('then authenticate with your Google account, click the gears icon on the bottom left.  Press "Generate QR Code"')
        raw_input('Press enter when you are done...')
        print('Starting Setup with WearScript (a QR scanner should be running now).  If a menu of options is visible on Glass then downswipe to close it.  Scan the code')
        self._screen_on()
        p = subprocess.Popen([self.adb, 'shell', 'am', 'start', '-n', 'com.dappervision.wearscript/.ui.SetupActivity'])
        r = p.wait()
        raw_input('Press enter when you are done...')

    def playground(self):
        print('Starting WearScript on Glass')
        self._screen_on()
        p = subprocess.Popen([self.adb, 'shell', 'am', 'start', '-n', 'com.dappervision.wearscript/.ui.ScriptActivity'])
        r = p.wait()
        url = 'https://api.wearscript.com'
        print('then press Ctrl+Enter (or Cmd+Enter on OS X) to run a script, you are all done')
        browser(url)
    
    def cleanup(self):
        print('Removing Working Directory: ' + self.directory)
        shutil.rmtree(self.directory)

class InstallerOSX(InstallerLinux):

    def __init__(self):
        super(InstallerOSX, self).__init__()
        self.adb_name = 'adb.osx'
        self.adb = os.path.join(self.directory, self.adb_name)
        self.urls = [URL + self.adb_name]


class InstallerWidows(InstallerLinux):

    def __init__(self):
        super(InstallerWindows, self).__init__()
        self.urls = [URL + 'AdbWinApi.dll',
                    URL + 'AdbWinUsbApi.dll',
                    URL + 'adb.exe']
        self.adb_name = 'adb.exe'
        self.adb = os.path.join(self.directory, self.adb_name)

def os_detector():
    uname = platform.uname()
    if uname[0] == 'Darwin' and uname[-2] == 'x86_64':
         return 'osx'
    elif uname[0] == 'Linux' and uname[-2] == 'x86_64':
        return 'linux64'
    return 'other'

def download(directory, url):
    print('Downloading: ' + url)
    urllib.urlretrieve(url, os.path.join(directory, os.path.basename(url)))

def main():
    curos = os_detector()
    print('Detected os[%s]' % str(curos))
    try:
        if curos == 'osx':
            installer = InstallerOSX()
        elif curos.startswith('linux'):
            installer = InstallerLinux()
        else:
            raise RuntimeError('Unknown OS')
        installer.download()
        installer.chmod_adb()
        installer.connect_glass()
        installer.push_apks()
        installer.authenticate()
        installer.playground()
    finally:
        installer.cleanup()

if __name__ == '__main__':
    main()
