Run Flask app:

    flask --app application run --reload

olcAccess to change:

    olcAccess: to attrs=userPassword
      by self write
      by group.exact="cn=webadmins,ou=Groups,dc=example,dc=com" write
      by anonymous auth
      by * none

    olcAccess: to *
      by self write
      by group.exact="cn=webadmins,ou=Groups,dc=example,dc=com" write
      by * read