from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import python_Testing_Utilities
import time


class local_helpers(testHelperSuperClass):
  pass
  
class test_kong_test(local_helpers):
  def test_noArgs(self):

    cmdToExecute = "./scripts/kong_update_or_add_cert_where_any_snis_match"
    expectedOutput = "Start of ./scripts/kong_update_or_add_cert_where_any_snis_match\n"
    expectedOutput += "Wrong number of arguments expected 5 - got 0\nRecieved args:\n['./scripts/kong_update_or_add_cert_where_any_snis_match']\n-"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_simplaAdd(self):
    self.deleteAllCerts()
    snis = "hosta.com,t.ac.uk,asd.com"
    
    cmdToExecute = "./scripts/kong_update_or_add_cert_where_any_snis_match " + self.kong_server + " " + snis + " ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"

    expectedOutput = "Start of ./scripts/kong_update_or_add_cert_where_any_snis_match\n"
    expectedOutput += "Found kong version " + self.expected_kong_version + "\n"
    expectedOutput += " updating where any cert matches any of " + snis + " (kong url " + self.kong_server + ")\n"
    expectedOutput += "Create cert for " + snis + " - 201\n"
    expectedOutput += "End of ./scripts/kong_update_or_add_cert_where_any_snis_match"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    resp2, respCode2 = self.callKongServiceWithFiles("/certificates/", None, "get", None, [200], None)
    self.assertEqual(len(resp2["data"]),1,msg="Wrong number of certs in server")
    
    if not python_Testing_Utilities.objectsEqual(resp2["data"][0]["snis"],snis.split(",")):
        print("Got SNI: " + str(resp2["data"][0]["snis"]))
        print("Expected SNI: " + snis)
        self.assertTrue(False,msg="SNIS not correct for cert")
