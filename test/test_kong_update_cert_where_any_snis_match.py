from TestHelperSuperClass import testHelperSuperClass
from executor import executeCommand
import python_Testing_Utilities
import time

#kong_update_cert_where_any_snis_match http://127.0.0.1:8001 hosta.com,t.ac.uk,asd.com ../examples/certs/server.crt ../examples/certs/server.key hosta.com,t.ac.uk,asd.com

class local_helpers(testHelperSuperClass):

  def addCert(self, certfile, privkeyfile, snis):
    files = {
      'cert': (certfile, open(certfile, 'rb')),
      'key': (privkeyfile, open(privkeyfile, 'rb'))
      ,'snis': (None, snis)
    }
    headers = {}
    resp, respCode = self.callKongServiceWithFiles("/certificates", headers, "post", files, [201], None)

    if self.expected_kong_version == "1.1.2":
        for x in snis.split(","):
            data = {
                'name': x
            }
            respSNI, respCodeSNI = self.callKongServiceWithFiles("/certificates/" + resp["id"] + "/snis", headers, "post", None, [201], data)


    #MAKE SURE CERT HAS BEEN ADDED
    resp2, respCode2 = self.callKongServiceWithFiles("/certificates", headers, "get", None, [200], None)
    found = False
    for x in resp2["data"]:
      if x["id"]==resp["id"]:
        #resp3, respCode3 = self.callKongServiceWithFiles("/certificates/" + x["id"] + "/snis", headers, "get", None, [200])
        #print("resp3", resp3)
        if not python_Testing_Utilities.objectsEqual(x["snis"],snis.split(",")):
            print("Got SNI: " + str(x["snis"]))
            print("Expected SNI: " + snis)
            self.assertTrue(False,msg="SNIS not correct for cert")
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

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url " + self.kong_server + ")\nEnd of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)



  def test_singleMatchingCert_OnlyOneCertInKong(self):
    self.deleteAllCerts()

    #Add a cert with SNI=hosta.com
    certID = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")

    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,asd.com (kong url " + self.kong_server + ")\n"
    expectedOutput += "Update cert for hosta.com (" + certID + ") - 200\n"
    expectedOutput += "End of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None
    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,asd.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

  def test_singleMatchingCert_MutipleOtherCertsInKong(self):
    self.deleteAllCerts()
    snis = "hosta.com,t.ac.uk,asd.com"

    #Add a cert with SNI=hosta.com
    certID = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostb.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostc.com")
    cartIDx = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostd.com")
    time.sleep(0.4)

    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " " + snis + " ./examples/certs/server.crt ./examples/certs/server.key " + snis
    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of " + snis + " (kong url " + self.kong_server + ")\n"
    expectedOutput += "Update cert for hosta.com (" + certID + ") - 200\n"
    expectedOutput += "End of ./scripts/kong_update_cert_where_any_snis_match"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, False)

    resp2, respCode2 = self.callKongServiceWithFiles("/certificates/" + certID, None, "get", None, [200], None)
    expected = ["hosta.com"]
    if not python_Testing_Utilities.objectsEqual(resp2["snis"],expected):
        print("Got SNI: " + str(resp2["snis"]))
        print("Expected SNI: " + str(expected))
        self.assertTrue(False,msg="SNIS not correct for cert")

  def test_mutipleMatchingCert_MutipleOtherCertsInKong(self):
    pass
    #Ignoring this test - I only use single sni's in my certs and this operation dosen't run consistantly
    '''
    self.deleteAllCerts()
    #hostc will error because all certs are associated with all sni's

    #Add a cert with SNI=hosta.com
    certIDa = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hosta.com")
    cartIDb = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostb.com")
    cartIDc = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostc.com")
    cartIDd = self.addCert("./examples/certs/server.crt", "./examples/certs/server.key", "hostd.com")

    expErr = "409"
    alreadyAsscMsg = "b'{\"message\":\"SNI \\'hosta.com\\' already associated with existing certificate (" + certIDa + ")\"}\\n'\n"
    if self.expected_kong_version == "1.1.2":
        expErr = "400"
        alreadyAsscMsg = "b'{\"message\":\"2 schema violations (cert: required field missing; key: required field missing)\",\"name\":\"schema violation\",\"fields\":{\"cert\":\"required field missing\",\"key\":\"required field missing\"},\"code\":2}'\n"

    cmdToExecute = "./scripts/kong_update_cert_where_any_snis_match " + self.kong_server + " hosta.com,t.ac.uk,hostc.com ./examples/certs/server.crt ./examples/certs/server.key hosta.com,t.ac.uk,asd.com"
    expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,hostc.com (kong url " + self.kong_server + ")\n"
    expectedOutput += "Update cert for hosta.com (" + certIDa + ") - 200\n"
    expectedOutput += "Update cert for hostc.com (" + cartIDc + ") - " + expErr + "\n"
    expectedOutput += "{'Date': 'Thu, 23 May 2019 07:50:57 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Access-Control-Allow-Origin': '*', 'Server': 'kong/0.13.1'}\n"
    expectedOutput += alreadyAsscMsg
    expectedOutput += "ERROR bad return"
    expectedErrorOutput = None


    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 2, True)

    #The order of hosta and hostc returned from the service call changes
    #in one case hostc will return first and no certs will be updated
    #in second case hosta will return first, have it's cert updated and then hostc will error
    outputArr = str(a.stdout,"utf-8").strip().strip('\n').split('\n')

    if len(outputArr) == 6:
        #hostc returned first and it errored
        expectedOutput = "Start of ./scripts/kong_update_cert_where_any_snis_match\n updating where any cert matches any of hosta.com,t.ac.uk,hostc.com (kong url " + self.kong_server + ")\n"
        expectedOutput += "Update cert for hostc.com (" + cartIDc + ") - " + expErr + "\n"
        expectedOutput += "{'Date': 'Thu, 23 May 2019 07:50:57 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Access-Control-Allow-Origin': '*', 'Server': 'kong/0.13.1'}\n"
        expectedOutput += alreadyAsscMsg
        expectedOutput += "ERROR bad return"
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
          if x != 3:
            #line 3 has a date in it so just don't check it
            self.assertEqual(outputArr[x], expectArr[x], msg="Error in output line " + str(x))
    elif len(outputArr) == 7:
        #hosta returned first was processed then hostc and it errored
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

        for x in [0,1,2,3,5]:
            #line 4 has a date in it so just don't check it
            #As order is different lines 1 and 2 may be swapped
            #ignoring line 6
            if x == 2:
                if not outputArr[x] == expectArr[x]:
                    if not outputArr[x] == expectArr[x+1]:
                        print("OutputArr:")
                        for xx in outputArr:
                          print(xx)
                        self.assertEqual(outputArr[x], expectArr[x], msg="ErrorNS1 in output line " + str(x+1) + " ALT:" + expectArr[x+1])
            if x == 3:
                if not outputArr[x] == expectArr[x]:
                    if not outputArr[x] == expectArr[x-1]:
                        print("OutputArr:")
                        for xx in outputArr:
                          print(xx)
                        self.assertEqual(outputArr[x], expectArr[x], msg="ErrorNS2 in output line " + str(x+1) + " ALT:" + expectArr[x-1])
            else:
                if outputArr[x] != expectArr[x]:
                  print("OutputArr:")
                  for xx in outputArr:
                    print(xx)
                self.assertEqual(outputArr[x], expectArr[x], msg="Error in output line " + str(x+1))

    else:
        self.assertFalse(True, msg="Wrong number of lines in output ")
    '''
