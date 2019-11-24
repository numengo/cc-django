__version__ = "{{ cookiecutter.version }}"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)

from simple_settings import LazySettings
settings = LazySettings('{{ cookiecutter.repo_name }}.config.settings', '{{ cookiecutter.app_name | upper }}.environ')

from ngoschema.utils import register_module
register_module('{{ cookiecutter.app_name }}')

__all__ = [
    'settings',
]
