import os
import sys
from typing import Union, Any

from InquirerPy.prompts import ListPrompt
from InquirerPy.utils import color_print

from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.version import version, release_date


def make_profile(measurements: list[SourceMeasurement]):
    result = [0, 0, 0, 0]
    for m in measurements:
        if m.value <= 15:
            result[0] += m.value
        elif m.value <= 30:
            result[1] += m.value
        elif m.value <= 60:
            result[2] += m.value
        else:
            result[3] += m.value
    return result


def merge_profiles(rc1: list[int], rc2: list[int]) -> list[int]:
    return [rc1[0] + rc2[0], rc1[1] + rc2[1], rc1[2] + rc2[2], rc1[3] + rc2[3]]


def path_has_suffix(path: str, suffixes: Union[str, list[str]]):
    dot_index = path.rfind('.')
    if dot_index >= 0:
        suffix = path[dot_index + 1:]
        if type(suffixes) == list:
            return suffix in suffixes
        else:
            return suffix == suffixes
    else:
        return False


def get_parent_folder(path: str) -> str:
    parts = path.split(os.path.sep)
    if len(parts) == 1:
        return '.'
    else:
        return os.path.sep.join(parts[0:-1])


def get_basename(path: str) -> str:
    parts = path.split(os.path.sep)
    return parts[-1]


def delete_indices(iterable: list, indices: list[int]) -> list[Any]:
    return [b for i, b in enumerate(iterable) if i not in indices]


def clear_screen() -> None:
    def isatty(stream) -> bool:
        try:
            return stream.isatty()
        except Exception:
            return False

    if not isatty(sys.stdout):
        return
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


def header(content: str):
    print_info(f'Code Limit (v. {version}, build date: {release_date})'.center(80))
    print(content)
    print_info()


def register_shortcut(prompt: ListPrompt, key: str, command: str, enable=True):
    @prompt.register_kb(key, filter=enable)
    def _(event):
        event.app.exit(result={'value': prompt.result_value, 'command': command})


def print_info(o: any = '', color='white'):
    msg = str(o)
    color_print([(color, msg)])
