from pathlib import Path
import winreg as wr

r"""
HKEY_CLASSES_ROOT
    foo
        (Default) = "URL: Foo Protocol"
        URL Protocol = ""
        DefaultIcon
            (Default) = "foo.exe,1"
        shell
            open
                command
                    (Default) = "C:\Program Files\example\foo.exe" "%1"
"""
PROTOCOL_NAME="sayonika"

ACCESS_RIGHTS = (wr.KEY_WRITE | wr.KEY_READ
                | wr.KEY_QUERY_VALUE | wr.KEY_SET_VALUE
                | wr.KEY_CREATE_SUB_KEY | wr.KEY_ENUMERATE_SUB_KEYS)
url_hand_path =  '"{}"'.format(Path.cwd()/'url_hand.py')
pythonpath = '"{}"'.format(Path.cwd()/'bin'/'python.exe')
program_launch = ' '.join([pythonpath, url_hand_path, '"%1"'])

# print ("ACCESS_RIGHTS: {}".format(repr(ACCESS_RIGHTS)))
with wr.CreateKeyEx(wr.HKEY_CLASSES_ROOT, PROTOCOL_NAME, 0, ACCESS_RIGHTS) as key:
    wr.SetValueEx(key, "", 0, wr.REG_SZ, "URL:Sayonika Protocol")
    wr.SetValueEx(key, "URL Protocol", 0, wr.REG_SZ, "")
    shell_key = wr.CreateKeyEx(key, "shell", 0, ACCESS_RIGHTS)
    open_key = wr.CreateKeyEx(shell_key, "open", 0, ACCESS_RIGHTS)
    command_key = wr.CreateKeyEx(open_key, "command", 0, ACCESS_RIGHTS)
    wr.SetValueEx(command_key, "", 0, wr.REG_SZ, program_launch)
print('Installed URL Protocol Handler "{}"'.format(PROTOCOL_NAME))
print("With shell command '{}'".format(program_launch))
