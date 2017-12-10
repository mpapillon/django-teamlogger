import os

import ldap3
from django.conf import settings
from django.utils.functional import cached_property
from ldap3.core.exceptions import LDAPException

from ldapab.exceptions import LDAPConnectionException, LDAPConnectionDoesNotExist
from ldapab.utils import DEFAULT_DIRECTORY_ALIAS, parse_ldap_url


class LDAPConnection(object):
    """
    Represent an LDAP directory connection.
    """

    def __init__(self, settings_dict, alias=DEFAULT_DIRECTORY_ALIAS):
        self.alias = alias

        self._connection = None
        self._settings_dict = settings_dict
        self._server = ldap3.Server(host=self._settings_dict['HOST'],
                                    port=int(self._settings_dict['PORT']),
                                    allowed_referral_hosts=[("*", True)])

    def open(self):
        """
        Opens a connection to the LDAP directory.
        :return: True if the connection is opened.
        """
        try:
            print('Try connection:', self._server)
            self._connection = ldap3.Connection(server=self._server,
                                                user=self._settings_dict['USER'],
                                                password=self._settings_dict['PASSWORD'],
                                                auto_bind=ldap3.AUTO_BIND_NO_TLS)
        except LDAPException as e:
            raise LDAPConnectionException from e

        return True

    def find_user(self, username):
        """
        Find a user in the directory and get his information.
        :param username: Username of the user to find
        :return: A dict containing user attributes values mapped to user model fields.
        """
        if not self._connection:
            return None

        attrs = self._settings_dict['ATTRIBUTES']
        sb = self._settings_dict['BASE']

        # Find the user into the LDAP directory
        username_attrs = attrs['username']
        for attr in username_attrs if isinstance(username_attrs, list) else [username_attrs]:
            filters = "(&({attr}={username}))".format(attr=attr, username=username)
            if not self._connection.search(sb, filters, attributes=ldap3.ALL_ATTRIBUTES):
                continue

            if len(self._connection.entries) == 0:
                continue

            break
        else:
            return None

        # Get user information
        entry = self._connection.entries[0]
        user = {'dn': entry.entry_dn}

        for field, ldap_attr in attrs.items():
            if isinstance(ldap_attr, list):
                for attr in ldap_attr:
                    if attr in entry:
                        user[field] = entry[attr]
                        break
                else:
                    user[field] = ''
            else:
                if ldap_attr in entry:
                    user[field] = entry[ldap_attr].value if entry[ldap_attr] else ''
                else:
                    user[field] = ''

        user['groups'] = self.get_user_groups(entry.entry_dn)

        return user

    def get_user_groups(self, user_dn):
        """Returns a list of group names where the user is a member."""
        sb = self._settings_dict['GROUP_BASE']
        if not sb:
            return []

        filters = "(&(member=%s))" % user_dn

        if self._connection.search(sb, filters, attributes=['cn']):
            return [g['cn'].value for g in self._connection.entries]
        else:
            return []

    def rebind(self, user_dn=None, password=None):
        return self._connection.rebind(user_dn, password)

    def close(self):
        """Closes a connection if opened."""
        if self._connection:
            self._connection.unbind()

    def __enter__(self):
        if self.open():
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LDAPConnectionHandler(object):
    def __init__(self, servers=None):
        self._servers = servers

    @cached_property
    def directories(self):
        if self._servers is None:
            self._servers = getattr(settings, 'LDAP_SERVERS', {})

        # If no default settings, checking in environment variables
        if os.getenv('LDAP_URL'):
            self._servers[DEFAULT_DIRECTORY_ALIAS].update(parse_ldap_url(os.getenv('LDAP_URL')))

        return self._servers

    def ensure_defaults(self, alias):
        """
        Puts the defaults into the settings dictionary for a given connection
        where no settings is provided.
        """
        try:
            conn = self.directories[alias]
        except KeyError:
            raise LDAPConnectionDoesNotExist("The connection %s doesn't exist" % alias)

        conn.setdefault('PORT', '389')
        conn.setdefault('ADMIN_GROUP', 'Administrators')
        conn.setdefault('ATTRIBUTES', {
            'username': ['uid', 'userid'],
            'email': ['mail', 'email'],
            'first_name': 'gn',
            'last_name': 'sn',
        })

        for setting in ['USER', 'PASSWORD', 'HOST', 'BASE', 'GROUP_BASE']:
            conn.setdefault(setting, '')

    def __getitem__(self, alias):
        if alias in self.__dict__:
            return self.__dict__[alias]

        self.ensure_defaults(alias)
        server = self.directories[alias]
        conn = LDAPConnection(server, alias)

        self.__dict__[alias] = conn

        return conn

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.directories)

    def all(self):
        return [self[alias] for alias in self]

    def close_all(self):
        for alias in self:
            connection = self.__dict__[alias]
            connection.close()
