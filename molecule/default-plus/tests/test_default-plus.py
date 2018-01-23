import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_vault_config(host):

    f = host.file('/etc/vault/config.hcl')

    assert f.exists
    assert f.is_file
    assert f.user == 'vault'
    assert f.group == 'vault'
    assert f.mode == 0o600
    assert f.contains('storage "consul" {')
    assert f.contains('address = "localhost:8500"')
    assert f.contains('scheme = "https"')
    assert f.contains('tls_cert_file = "/etc/vault/certs/vault-consul-client.crt"')
    assert f.contains('tls_key_file = "/etc/vault/private/vault-consul-client.key"')
    assert not f.contains('tls_ca_file')
    assert f.contains('listener "tcp" {')
    assert f.contains('tls_disable = 0')
    assert f.contains('tls_cert_file = "/etc/vault/certs/vault-composite.crt"')
    assert f.contains('tls_key_file = "/etc/vault/private/vault.key"')
    assert f.contains('address = "0.0.0.0:8200"')


def test_vault_running(host):

    ps = host.process.filter(user='vault', comm='vault')

    assert len(ps) == 1

    p = ps[0]

    assert p.args == ('/usr/local/sbin/vault server'
                      + ' -config /etc/vault/config.hcl')
