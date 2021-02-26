from ansible.errors import AnsibleError, AnsibleUndefinedVariable
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_text
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, **kwargs):
        variable_name = 'network_ip_management'

        if 'variables' in kwargs:
            self._templar.set_available_variables(kwargs['variables'])

        my_vars = getattr(self._templar, '_available_variables', {})
        self.set_options(direct=kwargs)

        if 'hostvars' not in my_vars:
            raise AnsibleError('Could not find host_vars structure!')
        host_vars = my_vars['hostvars']

        if 'groups' not in my_vars:
            raise AnsibleError('Could not find groups structure!')
        groups = my_vars['groups']

        groups_with_hosts = self._templar.template(groups, fail_on_undefined=True)

        hosts = set()
        for group in terms:
            if not isinstance(group, string_types):
                raise AnsibleError('Invalid group name, "%s" is not a string, its a %s' % (term, type(term)))
            group_hosts = groups_with_hosts.get(group, None)
            if group_hosts is None:
                raise AnsibleError('Could not find hosts group with name: %s' % group)
            hosts.update(group_hosts)

        result = set()
        for host in hosts:
            if host not in host_vars:
                raise AnsibleError('Could not find host: %s in host vars!' % host)
            value = host_vars[host].get(variable_name, None)
            if value is None:
                raise AnsibleError('Could not find variable: %s in the host: %s vars!' % (variable_name, host))
            result.add(to_text(value))

        return self._flatten(sorted(list(result)))

