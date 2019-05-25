from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  pass
  
class test_kong_test_delete_service(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_delete_service"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_delete_service\n"
    expectedOutput += "ERROR Wrong number of params\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_delete_a_Service_with_routes(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    
    #call install service and route
    cmdToExecute = "./scripts/kong_install_service_and_route"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " http"
    cmdToExecute += " www.host.com"
    cmdToExecute += " 80"
    cmdToExecute += " /"
    cmdToExecute += " " + route["protocol"]
    cmdToExecute += " " + route["host"]
    cmdToExecute += " " + route["path"]
    cmdToExecute += " GET"
    cmdToExecute += " null"
    cmdToExecute += " null"

    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_install_service_and_route\n"
    expectedOutput += "Installing service for \n"
    expectedOutput += "Invalid paramaters expecting 12 but 0 were supplied\n"
    expectedErrorOutput = None
    
    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    
    #not checking output, just checking function

    #check service is there
    resp, respCode = self.callKongService("/services/" + serviceName, {}, "get", None, [200])
    self.assertEqual(resp["name"],serviceName)    
    
    #delete service
    cmdToExecute = "./scripts/kong_delete_service " + self.kong_server + " " + serviceName
    expectedOutput = ""
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)
    
    #check service is not there
    resp, respCode = self.callKongService("/services/" + serviceName, {}, "get", None, [404])

