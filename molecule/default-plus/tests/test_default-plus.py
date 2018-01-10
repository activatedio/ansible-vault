import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_swap_disabled(host):

    o = host.check_output('free')

    assert "Swap:             0           0           0" in o


def test_swap_removed_from_fstab(host):

    assert not host.file('/etc/fstab').contains('swap')


def test_vault_downloaded(host):

    f = host.file('/usr/local/sbin/vault')

    assert f.exists
    assert f.is_file
    assert f.user == 'vault'
    assert f.group == 'vault'
    assert f.mode == 0o500


def test_vault_config_directory(host):

    f = host.file('/etc/vault')

    assert f.exists
    assert f.is_directory
    assert f.user == 'vault'
    assert f.group == 'vault'
    assert f.mode == 0o700


def test_vault_config(host):

    f = host.file('/etc/vault/config.hcl')

    assert f.exists
    assert f.is_file
    assert f.user == 'vault'
    assert f.group == 'vault'
    assert f.mode == 0o600

    assert f.contains('storage "inmem" {')
    assert f.contains('listener "tcp" {')
    assert f.contains('address = "127.0.0.1:8200"')
    assert f.contains('tls_disable = 1')


def test_vault_systemd_service(host):

    f = host.file('/lib/systemd/system/vault.service')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644
    assert f.contains('After=network.target')
    assert f.contains('User=vault')
    assert f.contains('ExecStart=/usr/local/sbin/vault server'
                      + ' -config /etc/vault/config.hcl')
    assert f.contains('WantedBy=multi-user.target')


def test_vault_running(host):

    ps = host.process.filter(user='vault', comm='vault')

    assert len(ps) == 1

    p = ps[0]

    assert p.args == ('/usr/local/sbin/vault server'
                      + ' -config /etc/vault/config.hcl')
