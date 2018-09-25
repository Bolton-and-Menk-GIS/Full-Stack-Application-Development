import ldap

VALID_CREDENTIALS = 'VALID_CREDENTIALS'
INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'

class SecurityHandler(object):
    def __init__(self, ldap_server, domain_name):
        self._ldap_server = ldap_server
        self.domain_name = domain_name

    def validate_AD(self, usr, pw='xxx'):
        usr = usr.split('\\')[-1]
        dn = '{}\\{}'.format(self.domain_name, usr.split('\\')[-1])  #username with domain validation
        print 'pw is: ', pw
        try:
            conn = ldap.initialize(self._ldap_server)
            conn.protocol_version = 3
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.simple_bind_s(dn, pw or 'xxx')  # need to be able to throw an error off an invalid pw
            return VALID_CREDENTIALS
        except ldap.INVALID_CREDENTIALS:
            return INVALID_CREDENTIALS