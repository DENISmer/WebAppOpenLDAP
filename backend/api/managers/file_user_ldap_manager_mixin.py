from api.managers.user_ldap_manager import UserFormatDN
from api.managers.file_user_ldap_manager import (ImageFileManager,
                                                  FileUserRetrieveLDAPManager,
                                                  FileUserModifyLDAPManager,)


class FileUserLDAPManagerMixin(
    UserFormatDN,
    ImageFileManager,
    FileUserRetrieveLDAPManager,
    FileUserModifyLDAPManager,
):
    pass
