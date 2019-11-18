__version__ = "{{ cookiecutter.version }}"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)

from simple_settings import LazySettings
settings = LazySettings('{{ cookiecutter.repo_name }}.config.settings', '{{ cookiecutter.project_slug | upper }}.environ')

from ngoschema.utils.module_loaders import load_module_templates, load_module_schemas

load_module_schemas('{{ cookiecutter.project_slug }}')
load_module_templates('{{ cookiecutter.project_slug }}')

__all__ = [
    'settings',
]
