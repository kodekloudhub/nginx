#! /bin/bash
#
# This script generates a self-signed cert with name $0 on the command line
# It generatges a key with the same name, but with a ,key extension
# Then it tells you what's in the cert.
# Finally, it verifies that the key and the cert match.

PAIR_NAME=$1
BITS=2048
DAYS=365
# Modify the RDNS to suit your individual preference (note my E-mail address is jeffsilverm@gmail.com)
RDNS="/C=US/ST=WA/L=Seattle/O=United\ Widgets/OU=IT\ Dept/CN=Jeff\ Silverman/emailAddress=jeffsilverm@gmail.com"
openssl genrsa -out ${PAIR_NAME},key $BITS

echo "Check the secret key  ${PAIR_NAME},key"
openssl rsa -noout -text -in ${PAIR_NAME},key

echo "Generating the self-signed certificate. ${PAIR_NAME},crt"
openssl req -new -x509 -nodes -sha256 -days $DAYS -subj "$RDNS" -key ${PAIR_NAME},key -out ${PAIR_NAME},crt

echo "Check the certificate: ${PAIR_NAME},crt"
openssl x509 -noout -text -in ${PAIR_NAME},crt

CERT_MD5=$( openssl x509 -noout -modulus -in  ${PAIR_NAME},crt | openssl md5 )
KEY_MD5=$( openssl rsa -noout -modulus -in  ${PAIR_NAME},key | openssl md5 )

echo "The key MD5 checksum is $KEY_MD5 . The cert MD5 checksum is $CERT_MD5 "
if [ "$CERT_MD5" == "$KEY_MD5" ]; then echo "Good!"; else echo "***BAD***"; exit 1; fi

