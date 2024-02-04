import unittest

from api.tgclient import TTClientsManager as TTCManager


class TestTTClientsManager(unittest.TestCase):
    def setUp(self) -> None:
        print("setUp")
        self.tel = "9212010568"

    def test_get_dialogs(self):
        try:
            ret = TTCManager.get_qrcode_url(self.tel)
            if "authorized" != ret:
                self.fail("test_get_dialogs:  fails: {}".format(ret))
            dialogs = TTCManager.get_dialogs(self.tel)
        except Exception as ex:
            self.fail("test_get_dialogs fails: {}".format(ex))


if __name__ == '__main__':
    unittest.main()
    