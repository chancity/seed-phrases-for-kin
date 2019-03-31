[![Build Status](https://travis-ci.org/chancity/seed-phrases-for-kin.svg)](https://travis-ci.org/chancity/seed-phrases-for-kin)

seed-phrases-for-kin
========================

This Python package provides a command-line script and a library module for
generating Kin accounts from BIP-0039/Electrum seed phrases. It performs
deterministic generation of Kin account keys from mnemonic seed phrases.
Each seed phrase may optionally be extended with custom words that play the
role of an additional passphrase.

seed-phrases-for-kin accepts two kinds of mnemonic seed phrases:
* seed phrases that comply with the BIP-0039 specification
  (https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), and
* seed phrases generated by the Electrum Bitcoin wallet (https://electrum.org/).

Since these are the two major standards for wallet seed phrases,
seed-phrases-for-kin accepts nearly all mnemonic phrases generated by
cryptocurrency wallets. Note, however, that this software does NOT perform
random generation of high-entropy seed phrases. Its main purpose is to allow
cryptocurrency wallet users to derive Kin account keys from high-entropy
seed phrases that they already have and that probably were created by their
wallets.

By following either BIP-0039 or Electrum, `seed-phrases-for-kin` 
derives a binary seed from a mnemonic seed phrase. Then it derives
Kin keys from the binary seed, as specified by SEP-0005
(https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md),
SLIP-0010 (https://github.com/satoshilabs/slips/blob/master/slip-0010.md) and
BIP-0044 (https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki).

# Installation
    pip3 install seed-phrases-for-kin

# Command-line usage
```
seed-phrase-to-Kin-keys -h
```
produces the following output:
```
usage: seed-phrase-to-Kin-keys [-h] [-n N] [-s] [-l] [-L LANG] [-v] [-F]

Generate Kin account keys from BIP-0039/Electrum seed phrases

optional arguments:
  -h, --help            show this help message and exit
  -n N, --n_accts N     show keys for multiple accounts (N > 0)
  -s, --show_seed       show the standard BIP-0039 or Electrum seed
  -l, --list_languages  list available languages for BIP-0039 phrases and exit
  -L LANG               language for BIP-0039 seed phrases (default: english)
  -v, --version         show program's version number and exit
  -F, --force           force keypair generation from phrase of unknown type

The default behavior of seed-phrase-to-Kin-keys is to show just the keys
for one Kin account (the primary account). By default, the binary seed
derived from the seed phrase is not shown. This behavior can be changed by the
'-n N' and '-s' switches.

```

## Examples

#### 1. Key derivation from a BIP-0039 seed phrase
```
$ seed-phrase-to-Kin-keys

Enter the seed phrase:
illness spike retreat truth genius clock brain pass fit cave bargain toe

Enter optional custom words (passphrase) to extend the seed phrase:


      seed phrase: 'illness spike retreat truth genius clock brain pass fit cave bargain toe'
     custom words: ''
 seed phrase type: BIP-0039

  primary account:
       public key: GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6
     private seed: SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN
     
```

#### 2. Same example as above, now showing the BIP-0039 seed and four accounts
```
$ seed-phrase-to-Kin-keys -s -n 4

Enter the seed phrase:
illness spike retreat truth genius clock brain pass fit cave bargain toe

Enter optional custom words (passphrase) to extend the seed phrase:


      seed phrase: 'illness spike retreat truth genius clock brain pass fit cave bargain toe'
     custom words: ''
 seed phrase type: BIP-0039
    BIP-0039 seed: e4a5a632e70943ae7f07659df1332160937fad82587216a4c64315a0fb39497ee4a01f76ddab4cba68147977f3a147b6ad584c41808e8238a07f6cc4b582f186

       account #0: ------------- this is the primary account --------------
       public key: GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6
     private seed: SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN

       account #1:
       public key: GBAW5XGWORWVFE2XTJYDTLDHXTY2Q2MO73HYCGB3XMFMQ562Q2W2GJQX
     private seed: SCEPFFWGAG5P2VX5DHIYK3XEMZYLTYWIPWYEKXFHSK25RVMIUNJ7CTIS

       account #2:
       public key: GAY5PRAHJ2HIYBYCLZXTHID6SPVELOOYH2LBPH3LD4RUMXUW3DOYTLXW
     private seed: SDAILLEZCSA67DUEP3XUPZJ7NYG7KGVRM46XA7K5QWWUIGADUZCZWTJP

       account #3:
       public key: GAOD5NRAEORFE34G5D4EOSKIJB6V4Z2FGPBCJNQI6MNICVITE6CSYIAE
     private seed: SBMWLNV75BPI2VB4G27RWOMABVRTSSF7352CCYGVELZDSHCXWCYFKXIX

```

#### 3. Key derivation from an Electrum seed phrase, showing the Electrum seed
```
$ seed-phrase-to-Kin-keys -s

Enter the seed phrase:
write long buzz fork domain forget punch child entry object load north

Enter optional custom words (passphrase) to extend the seed phrase:


      seed phrase: 'write long buzz fork domain forget punch child entry object load north'
     custom words: ''
 seed phrase type: Electrum standard
    Electrum seed: 4eb18cab8eaa91a4486bb0ef9ad814f3e40f946235ef7996c8e7b2a4186fdde3a841b501a12728d6ffe323c8272957e35334c684576087dee710d09d518bd9b2

  primary account:
       public key: GAF273TDSINGAMNL7OCMFYIBTUIRPFSXUQ6EYPJMVOOCQ3Z5ICSIBBLD
     private seed: SCCK6VFCREX4BFIHIHYX2O6AIIRSEID7HOI47YPB5XNSYLG7SI45D5RT

```
Note that `seed-phrase-to-Kin-keys` automatically detects the seed phrase
type. Electrum seed phrases have specific subtypes: old (pre 2.0) Electrum,
standard (Electrum 2.0 or later), segwit, and 2FA. In addition to
distinguishing BIP-0039 seed phrases from Electrum seed phrases, 
`seed-phrase-to-Kin-keys` shows the specific subtype of an Electrum seed
phrase. This information has no importance for the derivation of Kin
account keys, but it may be helpful to prevent typos from going unnoticed.

#### 4. Key derivation from an Electrum segwit seed phrase, showing the Electrum seed:

```
$ seed-phrase-to-Kin-keys -s 

Enter the seed phrase:
nerve museum sort subject call unable double rally wheat drip tiger kitchen

Enter optional custom words (passphrase) to extend the seed phrase:


      seed phrase: 'nerve museum sort subject call unable double rally wheat drip tiger kitchen'
     custom words: ''
 seed phrase type: Electrum segwit
    Electrum seed: 68d1e21953e934a7ff2f7d852e4a05d9fd12fbb86e1c49fb822c214a5ce57ee64c714b447ce23edb878cdc99d8adf4e29c3f9c9d237986ef9ac557fa60f37965

  primary account:
       public key: GBJM3LGVJLCM3YNH2IZ3I6U2HTAGKQVFITWWM5X3T4VE5CGNSDAKKG6K
     private seed: SALX6MN3OKWH6WIDYOUJTXOVJUWCYBHP7JNQUFUUD56WOATQVKKDMADE

```

#### 5. Key derivation from a phrase that is both a BIP-0039 seed phrase and an Electrum seed phrase

BIP-0039 and Electrum seed phrases are not disjoint sets. In the case of a
phrase that belongs to both sets, `seed-phrase-to-Kin-keys` performs the
BIP-0039 derivation and, if invoked with the '`-s`' option (as in the example
below), shows the BIP-0039 seed.
```
$ seed-phrase-to-Kin-keys -s 

Enter the seed phrase:
ivory hollow predict error front energy invite differ general depart repeat prize

Enter optional custom words (passphrase) to extend the seed phrase:
s0me p4ssphr4se         

      seed phrase: 'ivory hollow predict error front energy invite differ general depart repeat prize'
     custom words: 's0me p4ssphr4se'
 seed phrase type: BIP-0039 and Electrum standard
    BIP-0039 seed: c1a65a79988348c001593e22737f285dc49c054b2265394c5dbddf296c89bf5f0af5f8b3b6e231b8711314da6894a816320fb5cedbd99484f9da81dd9a261812

  primary account:
       public key: GDNRZZR5GU6QG5KQUWFE3WWD5L57JQAYC7CBLOIP5GQR2X7C4ZZJBWDR
     private seed: SDUNJQZRBESMERRIJCSIOKCS7K4VQKGM5BT6CLUX7FEQ3STVUAHIVH2V

```

# API usage

The deterministic generation of Kin account keys from a mnemonic seed
phrase is done in two steps:

1. derive a 64-byte binary seed from a mnemonic seed phrase;
2. generate Kin account keypairs from the binary seed.

#### 1. The first step
```python
    from seed_phrases_for_kin.seed_phrase_to_kin_keys import to_binary_seed
    my_seed_phrase = '...'
    my_passphrase = '...' 
    my_language = 'english' # or other language listed in
                            # https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
                            # NB: the language is relevant only in the case of a BIP39 seed phrase
    (binary_seed, seed_phrase_type) = to_binary_seed(my_seed_phrase,
                                                     my_passphrase,
                                                     my_language)
```
At this point, `seed_phrase_type` is one of the following strings:
- `'BIP-0039'`
- `'BIP-0039 and Electrum standard'`
- `'BIP-0039 and Electrum segwit'`
- `'BIP-0039 and Electrum 2FA'`
- `'Old (pre 2.0) Electrum'`
- `'Electrum standard'`
- `'Electrum segwit'`
- `'Electrum 2FA'`
- `'UNKNOWN'`

If `my_seed_phrase` is a BIP39-compliant phrase for `my_language`
(this condition covers the first four cases listed above), the
`to_binary_seed` call generates the binary seed as recommended by BIP39.
Otherwise, if `my_seed_phrase` is an Electrum seed phrase (this condition
covers the next four cases listed above), the `to_binary_seed` call generates
the binary seed by using Electrum's algorithm. Otherwise (this is the last
case listed above), the `to_binary_seed` call generates the binary seed in
a non-standard way.

#### 2. The second step
```python
    from seed_phrases_for_kin.key_derivation import account_keypair
    account_number = ... # an small unsigned integer (0 for the primary account)
    account_keypair = account_keypair(binary_seed, account_number)
```
The `account_keypair` call performs the key derivation specified by SEP-0005,
SLIP-0010, and BIP-0044.

#### 3. Alternative BIP39-only implementation of the first step
Note that the first step above handles both BIP39 and Electrum seed phrases.
If you do not need to handle Electrum seed phrases, then you can implement
the first step by using the package `mnemonic`
(https://github.com/trezor/python-mnemonic), which is the reference
implementation of BIP39:

```python
    from mnemonic import Mnemonic
    my_seed_phrase = '...'
    my_passphrase = '...' 
    my_language = 'english' # or other language listed in
                            # https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
    mnemo = Mnemonic(my_language)
    if mnemo.check(my_seed_phrase):
        # my_seed_phrase is a valid BIP39 phrase for my_language   
        binary_seed = Mnemonic.to_seed(my_seed_phrase, my_passphrase)
```
The second step remains unchanged.
