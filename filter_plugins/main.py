from collections.abc import Mapping
from copy import deepcopy

try:
    # AnsibleFilterTypeError was added in 2.10
    from ansible.errors import AnsibleFilterTypeError
except ImportError:
    from ansible.errors import AnsibleFilterError
    AnsibleFilterTypeError = AnsibleFilterError

from ansible.plugins.filter.core import flatten, to_nice_yaml


def render_crowdsec_config(config, server_enabled=True):
    if not isinstance(config, Mapping):
        raise AnsibleFilterTypeError("render_crowdsec_config requires a dictionary, got %s instead" % type(config))

    new_config = config

    if not server_enabled and config['api'] and config['api']['server']:
        new_config = deepcopy(new_config)
        del new_config['api']['server']

    return to_nice_yaml(new_config, indent=2)


class FilterModule(object):

    def filters(self):
        return {
            "render_crowdsec_config": render_crowdsec_config,
        }
