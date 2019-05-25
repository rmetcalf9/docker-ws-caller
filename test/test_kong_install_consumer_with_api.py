from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  def deleteConsumer(self, consumer_name):
    resp, respCode = self.callKongService("/consumers/" + consumer_name, {}, "get", None, [200, 404])
    if respCode == 404:
      return False

    resp, respCode = self.callKongService("/consumers/" + consumer_name, {}, "delete", None, [204])

    resp, respCode = self.callKongService("/consumers/" + consumer_name, {}, "get", None, [404])
    return True
  
class test_kong_install_consumer_with_api(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_install_consumer_with_api"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_install_consumer_with_api\n"
    expectedOutput += "ERROR Wrong number of params\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_invalidMode(self):
    cmdToExecute = "./scripts/kong_install_consumer_with_api " + self.kong_server + " invalid_mode consumer_name"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_install_consumer_with_api\n"
    expectedOutput += "ERROR Error mode must be DELETE or IGNORE\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_deleteMode_notAlreadyExist(self):    
    mode = "DELETE"
    consumer_name = "testNewConsumer"
    
    self.deleteConsumer(consumer_name)

    cmdToExecute = "./scripts/kong_install_consumer_with_api " + self.kong_server + " " + mode + " " + consumer_name
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_install_consumer_with_api\n"
    expectedOutput += "ERROR Error mode must be DELETE or IGNORE\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)

    # ignore output test function
    
    resp, respCode = self.callKongService("/consumers/" + consumer_name, {}, "get", None, [200])
    
    self.assertEqual(resp["username"],consumer_name, msg="Username not created")
    
    consumer_id = resp["id"]
    
    print(consumer_id)

    #check we have an api key
    resp, respCode = self.callKongService("/consumers/" + consumer_name + "/key-auth", {}, "get", None, [200])
    self.assertEqual(len(resp["data"]),1,msg="API key wrong")
    self.assertEqual(resp["data"][0]["consumer_id"],consumer_id)
    

  def test_deleteMode_AlreadyExist(self):
    self.assertTrue(False, msg="Not implemented")

#  def test_ignoreMode_AlreadyExist(self):
#  def test_ignoreMode_AlreadyExist(self):


