from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand

#kong_update_cert_where_any_snis_match http://127.0.0.1:8001 hosta.com,t.ac.uk,asd.com ../examples/certs/server.crt ../examples/certs/server.key hosta.com,t.ac.uk,asd.com

class local_helpers(testHelperSuperClass):
  def addCert(self, certfile, privkeyfile, snis):
    files = {
      'cert': (certfile, open(certfile, 'rb')),
      'key': (privkeyfile, open(privkeyfile, 'rb')),
      'snis': (None, snis)
    }
    headers = {}
    resp, respCode = self.callKongServiceWithFiles("/certificates", headers, "post", files, [201])
    return resp["id"]


class test_kong_test(local_helpers):
  def test_noArgs(self):

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\nWrong number of arguments expected 5 - got 0\nRecieved args:\n['./scripts/kong_update_cert_where_any_snis_match']\n-"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match"
    
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_noMatchingCerts(self):
    self.deleteAllCerts()

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url http://127.0.0.1:8381)\nEnd of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
     
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)



  def test_singleMatchingCert(self):
    self.deleteAllCerts()
    
    #Add a cert with SNI=hosta.com
    cartID = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url http://127.0.0.1:8381)\n"
    expectedOutput += "Update cert for hosta.com (" + cartID + ") - 200\n"
    expectedOutput += "End of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
     
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)
