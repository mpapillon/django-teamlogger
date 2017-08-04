from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group

from ldapab import connections
from ldapab.exceptions import LDAPConnectionException
from ldapab.models import DirectoryInfo, User
from ldapab.signals import populate_user


class LDAPAuthBackend(ModelBackend):
    """
    Authenticate users with an external LDAP directory.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        for conn in connections.all():
            alias = conn.alias
            directory = connections.directories[alias]

            try:
                conn.open()
                user_details = conn.find_user(username)

                # Check if the user exists in the directory
                if not user_details:
                    continue

                # Rebind with user credentials
                if not conn.rebind(user_details['dn'], password):
                    continue

                # Get or create the user entity
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                    user.save()

                # Updates the entity details
                user.email = user_details['email']
                user.first_name = user_details['first_name']
                user.last_name = user_details['last_name']

                if directory['GROUP_BASE']:
                    # Updates user groups
                    groups = []
                    for group_name in user_details['groups']:
                        if group_name == directory['ADMIN_GROUP']:
                            user.is_staff = True
                            user.is_superuser = True
                        else:
                            try:
                                group = Group.objects.get(name=group_name)
                            except Group.DoesNotExist:
                                group = Group(name=group_name)
                                group.save()
                            groups.append(group)

                    user.groups.clear()
                    user.groups.add(*groups)

                    # Removes Admin flag if user is demote
                    if directory['ADMIN_GROUP'] not in user_details['groups']:
                        user.is_staff = False
                        user.is_superuser = False

                user.save()

                # Updates source
                user.directory_info = DirectoryInfo(source=alias)
                user.directory_info.save()

                populate_user.send(self.__class__, user=user, attributes=user_details)

                return user
            except LDAPConnectionException:
                # Bind failed
                continue
            finally:
                conn.close()
