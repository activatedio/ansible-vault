#!/bin/bash

set -e

create_key_pair() {
  openssl genrsa -out $1.key 2048
  openssl req -new -key $1.key -out $1.csr \
    -subj "/C=US/ST=Washington/L=Some/O=Test/OU=IT Department/CN=$2"
  openssl x509 -req -in $1.csr -CA ca.pem -CAkey ca.key -CAcreateserial \
    -out $1.crt -days 1825 -sha256
}

openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1825 -out ca.pem \
  -subj "/C=US/ST=Washington/L=Some/O=Test/OU=IT Department/CN=*"

create_key_pair vault-server localhost
create_key_pair consul-server localhost
create_key_pair vault-consul-client localhost

