from TestHelperSuperClass import testHelperSuperClass
import uuid

class certHelpers(testHelperSuperClass):
  def createRandomCert(self):
    randID = str(uuid.uuid4())
    randomCertData = {
      "key": "random_cert_" + randID,
      "cert": "bbb",
      "snis": randID + ".x.com"
    }
    resp, respCode = self.callKongService("/certificates", {}, "put", randomCertData, [201])
    return randID + ".x.com", resp, respCode
    
  def countNumberOfCertsInKong(self):
    resp, respCode = self.callKongService("/certificates", {}, "get", None, [200])
    return resp["total"]

class test_kong_Delete_all_certs(certHelpers):
  def test_simpleTest(self):

    certData = []
    #Create 3 Certs
    for x in range(1,4):
      sni, resp, respCode = self.createRandomCert()
      certData.append({
        "id": resp["id"],
        "sni": sni,
        "seen": False #used for check
      })

    self.assertEqual(self.countNumberOfCertsInKong(),3,msg="Should be 3 certs in server - if more than there is a pre-test state issue")
    
    #EXECUTE TEST CODE
    cmdToExecute = "./scripts/kong_delete_all_certs " + self.kong_server
    expectedOutput = ""
    
    expectedOutput = expectedOutput + "\n"
    expectedOutput = expectedOutput + " deleting all certs for kong url " + self.kong_server + "\n"

    expectedErrorOutput = None
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    self.assertNotEqual(a.stdout, None)
    
    outputLines = a.stdout.decode().split("\n")
    self.assertEqual(len(outputLines),7, msg="Wrong number of lines output: \n" + a.stdout.decode())
    
    self.assertEqual(outputLines[0],"Start of ./scripts/kong_delete_all_certs", msg="Line 1 output wrong")
    self.assertEqual(outputLines[1]," deleting all certs for kong url " + self.kong_server, msg="Line 2 output wrong")
    #self.assertEqual(outputLines[2],"", msg="Line 3 output wrong")
    #self.assertEqual(outputLines[3],"", msg="Line 4 output wrong")
    #self.assertEqual(outputLines[4],"", msg="Line 5 output wrong")
    self.assertEqual(outputLines[5],"End of ./scripts/kong_delete_all_certs", msg="Line 6 output wrong")
    self.assertEqual(outputLines[6],"", msg="Line 7 output wrong")
    
    #lines 3,4 and 5 may be in any order
    for x in range(3,6):
      lineInOutput = outputLines[x-1]
      print("Lineinoutput:", lineInOutput)
      for y in certData:
        expected = "Deleting cert for ['" + y["sni"] + "'] (" + y["id"] + ")"
        if expected == lineInOutput:
          y["seen"] = True
          
    for x in certData:
      self.assertTrue(x["seen"],msg="Delete cert line not seen for sni " + x["sni"])
      
    self.assertEqual(self.countNumberOfCertsInKong(),0,msg="Failed to delete all certs")

