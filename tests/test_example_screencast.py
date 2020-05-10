import os
import filecmp
import autoscrub
from pathlib import Path

TEST_VIDEO_INPUT = "example_screencast.mp4"
TEST_VIDEO_OUTPUT = "example_screencast_scrub.mp4"
VALID_FILTERGRAPH = "example_screencast.txt"
VALID_DURATION = 48.57
VALID_LOUDNESS = {
    "I": -18.1,
    "Threshold": -39.2,
    "LRA": 7.3,
    "LRA low": -23.5,
    "LRA high": -16.2,
}

os.chdir(Path(__file__).parent.absolute())


def test_autoprocess(input=TEST_VIDEO_INPUT, filtergraph=VALID_FILTERGRAPH):
    """Runs autoscrub autoprocess --debug on TEST_VIDEO_INPUT

    Checks stdout and compares resulting filtergraph to known valid version
    """
    # Create output path
    suffix = Path(input).suffix
    output = input.replace(suffix, "_scrub" + suffix)

    # Run autoscrub autoprocess --debug input output
    p = autoscrub._agnostic_Popen(
        ["autoscrub", "autoprocess", "--debug", input, output]
    )
    _, stderr = autoscrub._agnostic_communicate(p)

    # Check stdout
    stdout = p.stdout.readlines()
    assert stdout[-4].strip() == b"[autoscrub:info] Done!"

    # Check filtergraph
    tmp = Path(stdout[-1].decode("utf8").split("at:")[-1].strip())
    assert filecmp.cmp(VALID_FILTERGRAPH, tmp)


def test_duration():
    """Checks duration of processed test video

    Checks duration of processed test video produced by autoscrub autoprocess
    is as expected.
    """
    assert autoscrub.getDuration(TEST_VIDEO_OUTPUT) == VALID_DURATION


def test_loudness():
    """Checks loudness properties of processed test video

    Checks loudness of test video produced by autoscrub autoprocess
    is as expected.
    """
    assert autoscrub.getLoudness(TEST_VIDEO_OUTPUT) == VALID_LOUDNESS
