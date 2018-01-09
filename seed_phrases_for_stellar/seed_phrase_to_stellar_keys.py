#!/usr/bin/python3
# -*- python-mode -*-
# -*- coding: UTF-8 -*-

# seed_phrase_to_stellar_keys
# Copyright (C) 2017 Francisco Reverbel
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def to_binary_seed(seed_phrase, passphrase='', language='english'):
    import hashlib
    import hmac
    from pbkdf2 import PBKDF2
    from mnemonic import Mnemonic
    from .electrum_mnemonic import normalize_text, \
                                   is_new_electrum_seed_phrase, \
                                   ELECTRUM_SEED_PREFIX_SW, \
                                   ELECTRUM_SEED_PREFIX_2FA, \
                                   electrum_seed_type
    
    seed_phrase = normalize_text(seed_phrase)
    passphrase = normalize_text(passphrase)
    
    m = Mnemonic(language)
    if m.check(seed_phrase):
        seed_phrase_type = 'BIP-0039'
        if is_new_electrum_seed_phrase(seed_phrase):
            seed_phrase_type += ' and Electrum standard'
        elif is_new_electrum_seed_phrase(seed_phrase, ELECTRUM_SEED_PREFIX_SW):
            seed_phrase_type += ' and Electrum segwit'
        elif is_new_electrum_seed_phrase(seed_phrase, ELECTRUM_SEED_PREFIX_2FA):
            seed_phrase_type += ' and Electrum 2FA'
        # salt for BIP-0039 seed
        salt = 'mnemonic' + passphrase
    else:
        seed_phrase_type = electrum_seed_type(seed_phrase)
        salt = ('electrum'
                if seed_phrase_type != 'UNKNOWN'
                else 'non-standard') + passphrase

    PBKDF2_ROUNDS = 2048
    binary_seed = PBKDF2(seed_phrase,
                         salt,
                         iterations = PBKDF2_ROUNDS,
                         macmodule = hmac,
                         digestmodule = hashlib.sha512).read(64)
    return (binary_seed, seed_phrase_type)


def account_message(i):
    msg = '\n       account #%d:' % i
    if i == 0:
        msg += ' ------------- this is the primary account --------------'
    return msg


def interactive_function(language, print_10_accs, print_binary_seed, force):
    from .electrum_mnemonic import bin_to_hexstr
    from .key_derivation import account_keypair
    
    seed_phrase = input('\nEnter the seed phrase:\n')
    passphrase = input('\nEnter optional custom words (passphrase)'
                       ' to extend the seed phrase:\n')
    print('')

    (binary_seed, seed_phrase_type) = to_binary_seed(seed_phrase,
                                                     passphrase,
                                                     language)
    
    print("      seed phrase: '" + seed_phrase + "'")
    print("     custom words: '" + passphrase + "'")
    print(' seed phrase type:', seed_phrase_type)
    if seed_phrase_type != 'UNKNOWN' or force:
        if print_binary_seed:
            if seed_phrase_type.startswith('BIP-0039'):
                print('    BIP-0039 seed:',  bin_to_hexstr(binary_seed))
            elif seed_phrase_type != 'UNKNOWN':
                print('    Electrum seed:',  bin_to_hexstr(binary_seed))
            else:
                print('non-standard seed:',  bin_to_hexstr(binary_seed))
        if print_10_accs:        
            for i in range(10):
                kp = account_keypair(binary_seed, i)
                print(account_message(i))
                print('       public key:',  kp.address().decode())
                print('     private seed:',  kp.seed().decode())
        else:
            kp = account_keypair(binary_seed, 0)
            print('\n  primary account:')
            print('       public key:',  kp.address().decode())
            print('     private seed:',  kp.seed().decode())
    print()


def main():
    import argparse
    import sys
    import os
    from mnemonic import Mnemonic
    from .version import __version__

    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))
    parser.add_argument(
        'language',
        nargs='?',
        default='english',
        help='language for BIP-0039 seed phrases (default: english)')
    parser.add_argument(
        '-m',
        '--multiple_accs', 
        help='show keys for ten accounts',
        action='store_true')
    parser.add_argument(
        '-s',
        '--show_seed', 
        help='show the standard BIP-0039 or Electrum seed',
        action='store_true')
    parser.add_argument(
        '-l',
        '--list_languages', 
        help='list available languages for BIP-0039 phrases and exit', 
        action='store_true')
    parser.add_argument(
        '-v',
        '--version', 
        action='version',
        version='%(prog)s version ' + __version__)
    parser.add_argument(
        '-F',
        '--force', 
        help='force keypair generation from phrase of unknown type', 
        action='store_true')
    args = parser.parse_args()
    
    if args.list_languages:
        lst = sorted(Mnemonic.list_languages())
        for language in lst:
            print(language)
    else:
        interactive_function(args.language, args.multiple_accs,
                             args.show_seed, args.force)