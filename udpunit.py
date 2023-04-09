import unittest
import udp

class TestDpd(unittest.TestCase):
    def test_checksum(self):
        self.assertEqual(udp.checksum_validation(10, 42, b'Welcome to IoT UDP Server'), 15307) # True payload is "Welcome to IoT UDP Server"
        self.assertEqual(udp.checksum_validation(5678, 1234, b'hello'), udp.checksum_validation(1234, 5678, b'hello')) # True : Sum of source and destination are the same
        self.assertNotEqual(udp.checksum_validation(10, 42, b'Welcome to the Server'), 15307) # False payload is not "Welcome to the Server"
        self.assertNotEqual(udp.checksum_validation(1234, 5678, b'hello'), udp.checksum_validation(5688, 1234, b'hello')) # False: Sum of source and destination are not the same ==> 1234 + 5678 =! 5688 + 1234
        
if __name__ == '__main__':
    print('\n\n\n----------------------------- UNIT TESTING ---------------------------\n')
    unittest.main()

