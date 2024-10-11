import pytest
from certbot_dns_glesys import DomainParts, GlesysAuthenticator, GlesysRecord
import unittest
from unittest.mock import MagicMock


# This config just sets all parameters to some value. It's just to make sure
# that the DNSAuthenticator constructor has all the parameters it might need
class PluginConfig:
    verb = "certonly"
    config_dir = "/tmp/cfg"
    work_dir = "/tmp/work"
    logs_dir = "tmp/log"
    cert_path = "./cert.pem"
    fullchain_path = "./chain.pem"
    chain_path = "./chain.pem"
    server = "https://acme-v02.api.letsencrypt.org/directory"


class GlesysTestAuthenticator(GlesysAuthenticator):
    def __init__(self, client):
        super().__init__(config=PluginConfig, name="dns-glesys")
        self._test_client = client

    def _get_glesys_client(self):
        return self._test_client


@pytest.mark.parametrize("full_domain", [
    "runfalk.se",
    "*.runfalk.se",
    "acme-v02.api.letsencrypt.org",
])
def test_domain_parts_init(full_domain):
    d = DomainParts(full_domain)
    assert d.domain == full_domain
    assert d.subdomain is None


def test_domain_parts_iter_variants():
    d = DomainParts("*.runfalk.se")
    expected_variants = {
        d,
        DomainParts("runfalk.se", "*"),
        DomainParts("se", "*.runfalk"),
    }
    assert set(d.iter_variants()) == expected_variants


def test_domain_parts_iter_variants_complex():
    d = DomainParts("acme-v02.api.letsencrypt.org")
    expected_variants = {
        d,
        DomainParts("api.letsencrypt.org", "acme-v02"),
        DomainParts("letsencrypt.org", "acme-v02.api"),
        DomainParts("org", "acme-v02.api.letsencrypt"),
    }
    assert set(d.iter_variants()) == expected_variants


def test_perform_cleanup_cycle():
    domain = "*.runfalk.se"  # Unused
    validation_domain = "_acme-challenge.runfalk.se"
    validation_key = "thisgoesinthetetxtrecord"

    glesys_mock = MagicMock()

    def split_domain(d):
        assert d == validation_domain
        return DomainParts("runfalk.se", "_acme-challenge")
    glesys_mock.split_domain.side_effect = split_domain

    auth = GlesysTestAuthenticator(glesys_mock)
    auth._perform(domain, validation_domain, validation_key)
    glesys_mock.add_record.assert_called_with(
        domain="runfalk.se",
        subdomain="_acme-challenge",
        type="TXT",
        data=validation_key,
        ttl=auth.ttl,
    )

    record_id = 20200411
    glesys_mock.list_records.return_value = [
        GlesysRecord(record_id, "runfalk.se", "_acme-challenge",
                     "TXT", validation_key, auth.ttl),
    ]
    auth._cleanup(domain, validation_domain, validation_key)
    glesys_mock.remove_record.assert_called_with(record_id)


class TestDomainParts(unittest.TestCase):

    def test_no_subdomain(self):
        """
        Test the behavior when there is no subdomain.
        
        It should yield the original domain with subdomain as None and
        the domain part after the last '.' as the second variant.
        """
        dp = DomainParts(domain="example.com")
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="example.com", subdomain=None),
            DomainParts(domain="com", subdomain="example"),
        ]

        self.assertEqual(variants, expected)

    def test_with_subdomain(self):
        """
        Test the behavior when a single subdomain is provided.
        
        It should yield the original domain with the subdomain, as well as 
        a variant that includes the subdomain and the main domain parts.
        """
        dp = DomainParts(domain="example.com", subdomain="www")
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="example.com", subdomain="www"),
            DomainParts(domain="com", subdomain="www.example"),
        ]

        self.assertEqual(variants, expected)

    def test_subdomain_with_multiple_parts(self):
        """
        Test the behavior when the subdomain consists of multiple parts.
        
        It should yield variants including all combinations of the subdomain 
        and domain parts.
        """
        dp = DomainParts(domain="example.com", subdomain="sub.www")
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="example.com", subdomain="sub.www"),
            DomainParts(domain="com", subdomain="sub.www.example"),
        ]

        self.assertEqual(variants, expected)

    def test_edge_case_empty_domain(self):
        """
        Test the behavior when the domain is empty.
        
        It should yield a single variant with an empty domain and subdomain.
        """
        dp = DomainParts(domain="", subdomain=None)
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="", subdomain=None)
        ]

        self.assertEqual(variants, expected)

    def test_edge_case_empty_subdomain(self):
        """
        Test the behavior when the subdomain is an empty string.
        
        It should yield the original domain with the empty subdomain, 
        along with a variant containing the domain part after the last '.'.
        """
        dp = DomainParts(domain="example.com", subdomain="")
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="example.com", subdomain=None),
            DomainParts(domain="com", subdomain=".example"),
        ]

        self.assertEqual(variants, expected)

    def test_edge_case_no_parts(self):
        """
        Test the behavior when the domain consists of a single part.
        
        It should yield a single variant with that part and no subdomain.
        """
        dp = DomainParts(domain="com", subdomain=None)
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="com", subdomain=None)
        ]

        self.assertEqual(variants, expected)

    def test_edge_case_only_subdomain(self):
        """
        Test the behavior when the domain is empty and only subdomain is provided.
        
        It should yield a single variant with an empty domain and the provided subdomain.
        """
        dp = DomainParts(domain="", subdomain="www")
        variants = list(dp.iter_variants())

        expected = [
            DomainParts(domain="", subdomain="www")
        ]

        self.assertEqual(variants, expected)
