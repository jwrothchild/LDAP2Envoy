from setuptools import setup, find_packages
setup(
        name = "envoyLdap",
        version = "0.1",
        packages = find_packages(),
        install_requires = ['PyYAML','requests','python-ldap'],
        author_email = "joanna@puppetlabs.com",
)
