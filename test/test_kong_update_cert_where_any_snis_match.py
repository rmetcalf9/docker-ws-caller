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
    
    #MAKE SURE CERT HAS BEEN ADDED
    resp2, respCode2 = self.callKongServiceWithFiles("/certificates", headers, "get", files, [200])
    found = False
    for x in resp2["data"]:
      if x["id"]==resp["id"]:
        return resp["id"]
    self.assertTrue(False, msg="After sucessful create of certificate a get request did not return it")


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



  def test_singleMatchingCert_OnlyOneCertInKong(self):
    self.deleteAllCerts()
    
    #Add a cert with SNI=hosta.com
    certID = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url http://127.0.0.1:8381)\n"
    expectedOutput += "Update cert for hosta.com (" + certID + ") - 200\n"
    expectedOutput += "End of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
     
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

  def test_singleMatchingCert_MutipleOtherCertsInKong(self):
    self.deleteAllCerts()
    
    #Add a cert with SNI=hosta.com
    certID = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostb.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostc.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostd.com")

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url " + self.kong_server + ")\n"
    expectedOutput += "Update cert for hosta.com (" + certID + ") - 200\n"
    expectedOutput += "End of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
     
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

  def test_mutipleMatchingCert_MutipleOtherCertsInKong(self):
    self.deleteAllCerts()
    #hostc will error because all certs are associated with all sni's
    
    #Add a cert with SNI=hosta.com
    certIDa = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")
    cartIDb = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostb.com")
    cartIDc = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostc.com")
    cartIDd = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostd.com")

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,hostc.com (kong url http://127.0.0.1:8381)\n"
    expectedOutput += "Update cert for hosta.com (" + certIDa + ") - 200\n"
    expectedOutput += "Update cert for hostc.com (" + cartIDc + ") - 409\n"
    expectedOutput += "{'Date': 'Thu, 23 May 2019 07:50:57 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Access-Control-Allow-Origin': '*', 'Server': 'kong/0.13.1'}\n"
    expectedOutput += "b'{\"message\":\"SNI \\'hosta.com\\' already associated with existing certificate (" + certIDa + ")\"}\\n'\n"
    expectedOutput += "ERROR bad return"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,hostc.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
     
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 2, True)
    
    outputArr = str(a.stdout,"utf-8").strip().strip('\n').split('\n')
    expectArr = expectedOutput.strip().strip('\n').split('\n')
    if len(outputArr) != len(expectArr):
      print("outputArr=")
      for x in range(0,len(outputArr)):
        print(str(x) + ":" + outputArr[x])
      print("\n--------------")
      print("expectArr=")
      for x in range(0,len(expectArr)):
        print(str(x) + ":" + expectArr[x])
    self.assertEqual(len(outputArr), len(expectArr), msg="Wrong output size")
    
    for x in range(0,len(outputArr)):
      if x != 4:
        #line 4 has a date in it so just don't check it
        self.assertEqual(outputArr[x], expectArr[x], msg="Error in output line " + str(x))
    


