from setuptools import setup, find_packages
setup(
        name = "envoyLdap",
        version = "0.1",
        packages = find_packages(),
        install_requires = ['yaml','requests','ldap']
        author_email = "joanna@puppetlabs.com",
)
