from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  pass


class test_kong_test_install_service_and_route(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_install_service_and_route"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_install_service_and_route\n"
    expectedOutput += "Installing service for \n"
    expectedOutput += "Invalid paramaters expecting 12 but 0 were supplied\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)


  def test_completlyNewService(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }

    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    #call install service and route
    self.createServiceAndRoute(serviceName, route)

    #not checking output, just checking function

    #check service is there
    resp, respCode = self.callKongService("/services/" + serviceName, {}, "get", None, [200])
    self.assertEqual(resp["name"],serviceName)

    #check route is there
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", None, [200])

    self.assertEqual(len(resp["data"]),1)
    self.assertEqual(resp["data"][0]["protocols"],[route["protocol"]])
    self.assertEqual(resp["data"][0]["hosts"],[route["host"]])
    self.assertEqual(resp["data"][0]["paths"],[route["path"]])


  def test_ExistingServiceWhichAlreadyHasARoute_repalceRouteIsFalse(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    newroute = {
      "protocol": "http",
      "host": "route.host222.com",
      "path": "/ppp222"
    }

    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    #call install service and route
    self.createServiceAndRoute(serviceName, route)

    self.createServiceAndRoute(serviceName, newroute)

    #not checking output, just checking function

    #check service is there
    resp, respCode = self.callKongService("/services/" + serviceName, {}, "get", None, [200])
    self.assertEqual(resp["name"],serviceName)

    #check route is there
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", None, [200])

    self.assertEqual(len(resp["data"]),1)
    #should still be old route as new route ignored
    self.assertEqual(resp["data"][0]["protocols"],[route["protocol"]])
    self.assertEqual(resp["data"][0]["hosts"],[route["host"]])
    self.assertEqual(resp["data"][0]["paths"],[route["path"]])

  def test_ExistingServiceWhichAlreadyHasARoute_repalceRouteIsTrue(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    newroute = {
      "protocol": "http",
      "host": "route.host222.com",
      "path": "/ppp222"
    }

    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    #call install service and route
    self.createServiceAndRoute(serviceName, route)

    cmdToExecute = "./scripts/kong_install_service_and_route"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " http"
    cmdToExecute += " www.host.com"
    cmdToExecute += " 80"
    cmdToExecute += " /"
    cmdToExecute += " " + newroute["protocol"]
    cmdToExecute += " " + newroute["host"]
    cmdToExecute += " " + newroute["path"]
    cmdToExecute += " GET"
    cmdToExecute += " null"
    cmdToExecute += " null"
    cmdToExecute += " true" #replace route

    expectedOutput = ""
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)

    #not checking output, just checking function

    #check service is there
    resp, respCode = self.callKongService("/services/" + serviceName, {}, "get", None, [200])
    self.assertEqual(resp["name"],serviceName)

    #check route is there
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", None, [200])

    self.assertEqual(len(resp["data"]),1)
    self.assertEqual(resp["data"][0]["protocols"],[newroute["protocol"]])
    self.assertEqual(resp["data"][0]["hosts"],[newroute["host"]])
    self.assertEqual(resp["data"][0]["paths"],[newroute["path"]])
