import six
import re
from distutils.version import LooseVersion

if six.PY3:
    from subprocess import Popen, PIPE
else:
    # backported subprocess module
    from subprocess32 import Popen, PIPE
__terminal_encoding = "utf-8"


def get_ffmpeg_version(strip_prefix=True):
    """Gets the version of ffmpeg, stripping prefix comprising alpha/dash
    characters, e.g. nightly build 'N-' prefix.
    Returns None if version cannot be determined."""
    command = ["ffmpeg", "-version"]
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout = p.stdout.readlines()
    line = stdout[0].decode(__terminal_encoding)
    version_match = re.match("ffmpeg version ([A-Za-z0-9\.\-]+)", line)
    if version_match:
        version_string = version_match.groups()[0]
        if strip_prefix:
            version = re.match("[A-Za-z\-]*([0-9\.]+[0-9])", version_string)
            if version:
                return version.groups()[0]
        else:
            return version_string
    return None


def check_ffmpeg_version(less_than="4.2"):
    """Check that the version of ffmpeg is less than the given
    version string, and print a warning if not or if the
    the ffmpeg version could not be determined.
    """
    version = get_ffmpeg_version(strip_prefix=True)
    if version is None:
        print(
            "[autoscrub:warning] Could not determine ffmpeg version. autoscrub requires ffmpeg < 4.2."
        )

    if LooseVersion(version) >= LooseVersion(less_than):
        print(
            "[autoscrub:warning] ffmpeg {} found. autoscrub requires ffmpeg < {}.".format(
                version, less_than
            )
        )


if __name__ == "__main__":
    check_ffmpeg_version()
