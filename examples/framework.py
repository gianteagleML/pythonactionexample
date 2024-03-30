'''sample framework file'''
import subprocess
import shlex
import json
import click


# create a function that runs subprocess and returns the output
def run_command(command):
    '''this is the function that runs the command and returns the output'''
    cmd = shlex.split(command)
    output = subprocess.check_output(cmd)
    return output

def run_lsblk(device):
    """
    Runs lsblk command and produces JSON output:

    lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT
    {
    "blockdevices": [
        {"name": "vda", "size": "59.6G", "type": "disk", "mountpoint": null,
            "children": [
                {"name": "vda1", "size": "59.6G", "type": "part", "mountpoint": "/etc/hosts"}
            ]
        }
    ]
    }
    """
    command = 'lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT'
    output = run_command(command)
    devices = json.loads(output)['blockdevices']
    for parent in devices:
        if parent['name'] == device:
            return parent
        for child in parent.get('children', []):
            if child['name'] == device:
                return child
    return None


@click.command()
@click.option('--verbose', '-v', is_flag=True)
@click.argument('device')

def main(device, verbose):
    '''this is the main function that runs the command and prints the output'''
    print(f"Device: {device}")
    print(f"Verbose: {verbose}")
    print(f"{run_lsblk(device)}")
