from os import path
import saml2
from saml2 import saml

BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
  "allow_unknown_attributes": True,

  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'https://lms.loc/saml2/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp': {
          "allow_unsolicited": True,
          'name': 'Federated Django sample SP',
          'name_id_format': saml.NAMEID_FORMAT_PERSISTENT,
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('https://lms.loc/saml2/acs/', saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ('https://lms.loc/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
                  ('https://lms.loc/saml2/ls/post', saml2.BINDING_HTTP_POST),
                ]
              },
          # attributes that this project need to identify a user
          'required_attributes': ['uid'],

          # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              'https://idp.example.com/simplesaml/saml2/idp/metadata.php': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SSOService.php',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SingleLogoutService.php',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [path.join(BASEDIR, 'remote_metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': path.join(BASEDIR, 'mycert.key'),  # private part
  'cert_file': path.join(BASEDIR, 'mycert.pem'),  # public part

  # own metadata settings
  # 'contact_person': [
  #     {'given_name': 'Lorenzo',
  #      'sur_name': 'Gil',
  #      'company': 'Yaco Sistemas',
  #      'email_address': 'lgs@yaco.es',
  #      'contact_type': 'technical'},
  #     {'given_name': 'Angel',
  #      'sur_name': 'Fernandez',
  #      'company': 'Yaco Sistemas',
  #      'email_address': 'angel@yaco.es',
  #      'contact_type': 'administrative'},
  #     ],
  # # you can set multilanguage information here
  # 'organization': {
  #     'name': [('Yaco Sistemas', 'es'), ('Yaco Systems', 'en')],
  #     'display_name': [('Yaco', 'es'), ('Yaco', 'en')],
  #     'url': [('http://www.yaco.es', 'es'), ('http://www.yaco.com', 'en')],
  #     },
  'valid_for': 24,  # how long is our metadata valid
  }

SAML_CONFIG_LOADER = 'djangosaml2.conf.config_settings_loader_pepper'
