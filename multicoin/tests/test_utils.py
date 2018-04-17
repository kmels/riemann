import unittest
from .. import utils
from . import helpers


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_i2le(self):
        self.assertEqual(utils.i2le(0), b'\x00')
        self.assertEqual(utils.i2le(0xff), b'\xff')
        self.assertEqual(utils.i2le(0x0100), b'\x00\x01')
        self.assertEqual(utils.i2le(0xabcdef), b'\xef\xcd\xab')

    def test_i2le_padded(self):
        self.assertEqual(utils.i2le_padded(0, 4), b'\x00' * 4)
        self.assertEqual(utils.i2le_padded(0xff, 1), b'\xff')
        self.assertEqual(utils.i2le_padded(0x0100, 8),
                         b'\x00\x01\x00\x00\x00\x00\x00\x00')
        self.assertEqual(utils.i2le_padded(0xabcdef, 5),
                         b'\xef\xcd\xab\x00\x00')

    def test_le2i(self):
        self.assertEqual(utils.le2i(b'\x00' * 4), 0)
        self.assertEqual(utils.le2i(b'\xff'), 0xff)
        self.assertEqual(utils.le2i(b'\x00\x01\x00\x00\x00\x00\x00\x00'),
                         0x0100)
        self.assertEqual(utils.le2i(b'\xef\xcd\xab\x00\x00'), 0xabcdef)

    def test_be2i(self):
        self.assertEqual(utils.be2i(b'\x00' * 4), 0)
        self.assertEqual(utils.be2i(b'\xff'), 0xff)
        self.assertEqual(utils.be2i(b'\x00\x01\x00\x00\x00\x00\x00\x00'),
                         0x01000000000000)
        self.assertEqual(utils.be2i(b'\xef\xcd\xab\x00\x00'), 0xefcdab0000)

    def test_change_endianness(self):
        self.assertEqual(utils.change_endianness(b'\x00'), b'\x00')
        self.assertEqual(utils.change_endianness(b'\x00\xaa'), b'\xaa\x00')
        self.assertEqual(utils.change_endianness(b'\xff'), b'\xff')
        self.assertEqual(utils.change_endianness(b'\x00\xab\xcd\xef'),
                         b'\xef\xcd\xab\x00')

    def test_rmd160(self):
        '''
        https://homes.esat.kuleuven.be/~bosselae/ripemd160.html
        '''
        self.assertEqual(
            utils.rmd160(b''),
            bytes.fromhex('9c1185a5c5e9fc54612808977ee8f548b2258d31'))
        self.assertEqual(
            utils.rmd160('message digest'.encode('utf-8')),
            bytes.fromhex('5d0689ef49d2fae572b881b123a85ffa21595f36'))

    def test_sha256(self):
        '''
        https://www.di-mgt.com.au/sha_testvectors.html
        '''
        self.assertEqual(
            utils.sha256(b''),
            bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'))  # noqa: E501
        self.assertEqual(
            utils.sha256('abc'.encode('utf-8')),
            bytes.fromhex('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'))  # noqa: E501
        self.assertEqual(
            utils.sha256(helpers.P2WSH_SERIALIZED_SCRIPT),
            helpers.P2WSH_SCRIPT_HASH)

    def test_hash160(self):
        self.assertEqual(
            utils.hash160(bytes.fromhex(helpers.PK_0)),
            helpers.PKH_0)
        self.assertEqual(
            utils.hash160(bytes.fromhex(helpers.PK_1)),
            helpers.PKH_1)
        self.assertEqual(
            utils.hash160(helpers.P2WPKH_PUBKEY),
            helpers.P2WPKH_PKH)

    def test_hash256(self):
        '''
        http://www.herongyang.com/Bitcoin/Block-Data-Calculate-Double-SHA256-with-Python.html
        '''
        self.assertEqual(
            utils.hash256(b'\x00'),
            bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a'))  # noqa: E501
        self.assertEqual(
            utils.hash256('abc'.encode('utf-8')),
            bytes.fromhex('4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358'))  # noqa: E501