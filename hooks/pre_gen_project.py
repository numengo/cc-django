"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment.

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""
from __future__ import print_function

import sys

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

app_name = "{{ cookiecutter.app_name }}"
if hasattr(app_name, "isidentifier"):
    assert (
        app_name.isidentifier()
    ), "'{}' project slug is not a valid Python identifier.".format(app_name)

assert (
    app_name == app_name.lower()
), "'{}' project slug should be all lowercase".format(app_name)

assert (
    "\\" not in "{{ cookiecutter.full_name }}"
), "Don't include backslashes in author name."

if "{{ cookiecutter.use_docker }}".lower() == "n":
    python_major_version = sys.version_info[0]
    if python_major_version == 2:
        print(
            WARNING + "You're running cookiecutter under Python 2, but the generated "
            "project requires Python 3.7+. Do you want to proceed (y/n)? " + TERMINATOR
        )
        yes_options, no_options = frozenset(["y"]), frozenset(["n"])
        while True:
            choice = raw_input().lower()
            if choice in yes_options:
                break

            elif choice in no_options:
                print(INFO + "Generation process stopped as requested." + TERMINATOR)
                sys.exit(1)
            else:
                print(
                    HINT
                    + "Please respond with {} or {}: ".format(
                        ", ".join(
                            ["'{}'".format(o) for o in yes_options if not o == ""]
                        ),
                        ", ".join(
                            ["'{}'".format(o) for o in no_options if not o == ""]
                        ),
                    )
                    + TERMINATOR
                )

if (
    "{{ cookiecutter.use_whitenoise }}".lower() == "n"
    and "{{ cookiecutter.cloud_provider }}" == "None"
):
    print(
        "You should either use Whitenoise or select a Cloud Provider to serve static files"
    )
    sys.exit(1)

languages = "{{ cookiecutter.languages }}".replace(' ', '').split(',')
for lang in languages:
    assert len(lang) == 2 and lang.lower() == lang, "Each language code shall consist of two lowercase letters, '" + lang + "' does not."
if "{{ cookiecutter.use_i18n }}" == 'y':
    assert len(languages) > 1, "'use_i18n' is set with less than two languages, which doesn't make sense."
else:
    assert len(languages) == 1, "If 'use_i18n' is unset, only one language shall be specified in 'languages'."
