"""Orginal Author: Douglas Creager <dcreager@dcreager.net>"""
from subprocess import Popen, PIPE


def call_git_describe():
    try:
        p = Popen(['git', 'describe'],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()
        line = line[0].decode().strip()
        return line
    except BaseException:
        return None


def read_release_version():
    try:
        with open("RELEASE-VERSION", "r") as f:
            version = f.readlines()[0]
            return version.strip()
    except BaseException:
        return None


def write_release_version(version):
    with open("RELEASE-VERSION", "w") as f:
        f.write("%s\n" % version)


def get_version(short=True):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()

    # First try to get the current version using “git describe”.
    version = call_git_describe()

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        write_release_version(version)

    # Finally, return the current version.
    if short:
        version = version.rsplit("-", 1)[0].replace("-", ".")
    return str(version)


if __name__ == "__main__":
    print(get_version())
