import argparse

from apricot import ApricotServer
from apricot.oauth_clients import OAuthBackend

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Apricot",
        description="Apricot is a proxy for delegating LDAP requests to an OpenID Connect backend.",
    )
    parser.add_argument("-b", "--backend", type=OAuthBackend, help="Which backend to use")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to run on")
    parser.add_argument("-i", "--client-id", type=str, help="OAuth client ID")
    parser.add_argument("-s", "--client-secret", type=str, help="OAuth client secret")
    parser.add_argument("-t", "--tenant-id", type=str, help="Microsoft Entra tenant id")

    args = parser.parse_args()

    # Create the Apricot server
    reactor = ApricotServer(**vars(args))
    reactor.run()
