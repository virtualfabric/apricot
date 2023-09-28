from typing import cast

from ldaptor.inmemory import ReadOnlyInMemoryLDAPEntry
from ldaptor.protocols.ldap.distinguishedname import (
    DistinguishedName,
    RelativeDistinguishedName,
)
from ldaptor.protocols.ldap.ldaperrors import (
    LDAPEntryAlreadyExists,
    LDAPInvalidCredentials,
)
from twisted.internet import defer
from twisted.python import log

from apricot.oauth import LDAPAttributeDict, OAuthClient


class OAuthLDAPEntry(ReadOnlyInMemoryLDAPEntry):
    dn: DistinguishedName
    attributes: LDAPAttributeDict

    def __init__(
        self,
        dn: DistinguishedName | str,
        attributes: LDAPAttributeDict,
        oauth_client: OAuthClient | None = None,
    ) -> None:
        """
        Initialize the object.

        @param dn: Distinguished Name of the object
        @param attributes: Attributes of the object.
        @param oauth_client: An OAuth client used for binding
        """
        self.oauth_client_ = oauth_client
        if not isinstance(dn, DistinguishedName):
            dn = DistinguishedName(stringValue=dn)
        super().__init__(dn, attributes)

    def __str__(self) -> str:
        output = bytes(self.toWire()).decode("utf-8")
        for child in self._children.values():
            try:
                # Indent children by two spaces
                indent = "  "
                output += (
                    f"{indent}{str(child).strip()}".replace("\n", f"\n{indent}")
                    + "\n\n"
                )
            except TypeError:
                pass
        return output

    @property
    def oauth_client(self) -> OAuthClient:
        if not self.oauth_client_:
            if hasattr(self._parent, "oauth_client"):
                self.oauth_client_ = self._parent.oauth_client
        if not isinstance(self.oauth_client_, OAuthClient):
            msg = f"OAuthClient is of incorrect type {type(self.oauth_client_)}"
            raise TypeError(msg)
        return self.oauth_client_

    @property
    def username(self) -> str:
        username = self.dn.split()[0].getText().split("CN=")[1]
        domain = self.dn.getDomainName()
        return f"{username}@{domain}"

    def add_child(
        self, rdn: RelativeDistinguishedName | str, attributes: LDAPAttributeDict
    ) -> "OAuthLDAPEntry":
        if isinstance(rdn, str):
            rdn = RelativeDistinguishedName(stringValue=rdn)
        try:
            output = self.addChild(rdn, attributes)
        except LDAPEntryAlreadyExists:
            log.msg(f"Refusing to add child '{rdn.getText()}' as it already exists.")
            output = self._children[rdn.getText()]
        return cast(OAuthLDAPEntry, output)

    def bind(self, password: bytes) -> defer.Deferred["OAuthLDAPEntry"]:
        def _bind(password: bytes) -> "OAuthLDAPEntry":
            s_password = password.decode("utf-8")
            if self.oauth_client.verify(username=self.username, password=s_password):
                return self
            msg = f"Invalid password for user '{self.username}'."
            raise LDAPInvalidCredentials(msg)

        return defer.maybeDeferred(_bind, password)
