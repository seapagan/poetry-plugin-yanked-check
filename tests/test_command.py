"""Tests for the command module."""

from pathlib import Path

from poetry_plugin_check_yanked.command import (
    DEFAULT_TIMEOUT,
    CheckYankedCommand,
)
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture


def test_check_pickledb_init(
    get_fs: FakeFilesystem, mocker: MockerFixture, mock_data_dir: MockerFixture
) -> None:
    """Test the initialization of the CheckYankedCommand class."""
    mock_pickledb_load = mocker.patch("pickledb.load")
    mock_pickledb_load.return_value = mocker.Mock()

    CheckYankedCommand()

    mock_pickledb_load.assert_called_once_with(
        Path("/mocked/path") / "cache.db", False
    )


def test_instantiate_class(
    mocker: MockerFixture, yank_class: CheckYankedCommand
) -> None:
    """Test that the yank_class fixture returns the CheckYankedCommand class.

    Also ensure that the __init__ side-effects are applied.
    """
    assert isinstance(yank_class, CheckYankedCommand)

    assert yank_class.cache is not None
    assert yank_class.yanked_packages == []
    assert yank_class._data_dir == Path("/mocked/path")  # noqa: SLF001
    assert Path("/mocked/path").exists()
    assert Path("./poetry.lock").exists()

    assert yank_class.timeout_seconds == DEFAULT_TIMEOUT
