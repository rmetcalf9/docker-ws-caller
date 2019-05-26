from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  pass

class test_kong_add_route_to_service(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_add_route_to_service"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_route_to_service\n"
    expectedOutput += "Installing new route for service \n"
    expectedOutput += "Invalid paramaters expecting 8 but 0 were supplied\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)

  def test_normal(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    addedroute = {
      "protocol": "http",
      "host": "route.addedhost.com",
      "path": "/ppp"
    }
    addedroute2 = {
      "protocol": "http",
      "host": "route.addedhost.com",
      "path": "/ppp"
    }    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    serviceResp = self.createServiceAndRoute(serviceName, route)
    postData = {
      "strip_path": False,
      "preserve_host": False,
      "service": {"id": serviceResp["serviceID"]},
      "protocols": [addedroute["protocol"]],
      "hosts": [addedroute["host"]],
      "paths": [addedroute["path"]]
      #append_comma_seperated_value methods ${ROUTE_METHODS}
    }

    resp, respCode = self.callKongService("/routes", {}, "post", postData, [201])

    #Get list of routes for this service`
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),2,msg="Setup routes not right")

    #Add a third route using script to be tested
    cmdToExecute = "./scripts/kong_add_route_to_service"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " " + addedroute2["protocol"]
    cmdToExecute += " " + addedroute2["host"]
    cmdToExecute += " " + addedroute2["path"]
    cmdToExecute += " " + "GET" #ROUTE_METHODS
    cmdToExecute += " " + "null" #ROUTE_STRIP_PATH
    cmdToExecute += " " + "null" #ROUTE_PRESERVE_HOST

    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_route_to_service\n"
    expectedOutput += "Installing new route for service \n"
    expectedOutput += "Invalid paramaters expecting 8 but 0 were supplied\n"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, skipOutputChecks=True)

    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),3,msg="Route not added")


  def test_invalidServiceName(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    addedroute = {
      "protocol": "http",
      "host": "route.addedhost.com",
      "path": "/ppp"
    }
    addedroute2 = {
      "protocol": "http",
      "host": "route.addedhost.com",
      "path": "/ppp"
    }    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    serviceResp = self.createServiceAndRoute(serviceName, route)
    postData = {
      "strip_path": False,
      "preserve_host": False,
      "service": {"id": serviceResp["serviceID"]},
      "protocols": [addedroute["protocol"]],
      "hosts": [addedroute["host"]],
      "paths": [addedroute["path"]]
      #append_comma_seperated_value methods ${ROUTE_METHODS}
    }

    resp, respCode = self.callKongService("/routes", {}, "post", postData, [201])

    #Get list of routes for this service`
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),2,msg="Setup routes not right")

    #Add a third route using script to be tested
    cmdToExecute = "./scripts/kong_add_route_to_service"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + "INVALIDSERVICENAME"
    cmdToExecute += " " + addedroute2["protocol"]
    cmdToExecute += " " + addedroute2["host"]
    cmdToExecute += " " + addedroute2["path"]
    cmdToExecute += " " + "GET" #ROUTE_METHODS
    cmdToExecute += " " + "null" #ROUTE_STRIP_PATH
    cmdToExecute += " " + "null" #ROUTE_PRESERVE_HOST

    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_add_route_to_service\n"
    expectedOutput += "Installing new route for service INVALIDSERVICENAME\n"
    expectedOutput += "ERROR Service not found in kong\n"
    expectedOutput += "Output: curl: (22) The requested URL returned error: 404 Not Found"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, skipOutputChecks=False)

    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),2,msg="Route was added but should not have been")
