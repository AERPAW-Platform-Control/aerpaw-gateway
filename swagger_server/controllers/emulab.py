import subprocess
import tempfile
import os
import shlex
from flask import abort

CMD_PREFIX = os.getenv('SSH_CMD')
ADMIN = os.getenv('EMULAB_ADMIN')
PARSE_PL_FILE = os.getenv('PARSE_PL_FILE')


def send_request(emulab_cmd):
    print(emulab_cmd)
    emulab_cmd_args = shlex.split(emulab_cmd)
    try:
        emulab_stdout = subprocess.check_output(emulab_cmd_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        print(err.output)
        if b'Profile does not exist' in err.output:
            abort(404, description="Profile does not exist")
        elif b'unknown user' in err.output:
            abort(404, description="Unknown user")
        elif b'No such project' in err.output:
            abort(404, description="No such project")
        elif b'No such instance' in err.output:
            abort(404, description="No such instance")
        elif b'Search Failed' in err.output:
            abort(404, description="Search Failed")
        else:
            abort(500, description=err.output.decode("utf-8"))
    print(emulab_stdout)
    return emulab_stdout


def parse_response(emulab_output):
    print(emulab_output)
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(emulab_output)
    fp.close()
    try:
        json_string = subprocess.check_output([PARSE_PL_FILE, fp.name],
                                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        os.unlink(fp.name)
        print(err.output)
        return err.output

    os.unlink(fp.name)
    print(json_string)
    return json_string
