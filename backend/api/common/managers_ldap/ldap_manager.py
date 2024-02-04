import ssl

from flask_ldap3_login import LDAP3LoginManager
from ldap3 import Tls

from backend.api.config.ldap import config


class ManagerLDAP(LDAP3LoginManager):  # Singleton
    _instance = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_config(config)
        self.tls_ctx = None
        self._add_tls_ctx()

        for host in config['LDAP_HOSTS']:
            self.add_server(
                hostname=host,
                port=config['LDAP_PORT'],
                use_ssl=config['LDAP_USE_SSL'],
                tls_ctx=self.tls_ctx,
            )

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(ManagerLDAP, cls) \
                .__new__(cls, *args, **kwargs)
        return cls._instance[cls]

    def _add_tls_ctx(self):
        if config['LDAP_USE_SSL']:
            self.tls_ctx = Tls(
                validate=ssl.CERT_REQUIRED,
                version=ssl.PROTOCOL_TLSv1,
                ca_certs_file=config['CERT_PATH']
            )
