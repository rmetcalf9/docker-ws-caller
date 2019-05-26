from TestHelperSuperClass import testHelperSuperClass

class local_helpers(testHelperSuperClass):
  pass

class test_kong_delete_all_routes_apart_from_one(local_helpers):
  def test_noArgs(self):
    cmdToExecute = "./scripts/kong_delete_all_routes_apart_from_one"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_delete_all_routes_apart_from_one\n"
    expectedOutput += "Wrong number of arguments expected 3 - got 0\n"
    expectedOutput += "Recieved args:\n"
    expectedOutput += "['./scripts/kong_delete_all_routes_apart_from_one']\n-"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [1], 1, False)


  def test_normalOperation(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    routesToAdd = []
    for x in range(0,5):
        #print(":" + str(x).strip() + ":")
        routesToAdd.append({
          "protocol": "http",
          "host": "route.host" + str(x).strip() + ".com",
          "path": "/ppp"
        })

    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    serviceResp = self.createServiceAndRoute(serviceName, route)
    #print("serviceResp:", serviceResp)

    #Add Extra routes to the services
    for curroute in routesToAdd:
      postData = {
        "strip_path": False,
        "preserve_host": False,
        "service": {"id": serviceResp["serviceID"]},
        "protocols": [curroute["protocol"]],
        "hosts": [curroute["host"]],
        "paths": [curroute["path"]]
        #append_comma_seperated_value methods ${ROUTE_METHODS}
      }
      resp, respCode = self.callKongService("/routes", {}, "post", postData, [201])

    #Get list of routes for this service`
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),6,msg="Setup routes not right")

    #Call function
    cmdToExecute = "./scripts/kong_delete_all_routes_apart_from_one"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " " + serviceResp["routeID"]
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_delete_all_routes_apart_from_one\n"
    expectedOutput += "Wrong number of arguments expected 3 - got 0\n"
    expectedOutput += "Recieved args:\n"
    expectedOutput += "['./scripts/kong_delete_all_routes_apart_from_one']\n-"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)


    #Check only the one route we wanted lasts
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),1,msg="Should only be a single route remaining")

    #Check for actual route
    self.assertEqual(resp["data"][0]["hosts"][0],route["host"],msg="Wrong route remains")

  def test_passingIDThatDoesNotExist(self):
    serviceName = "TestServiceName"
    route = {
      "protocol": "http",
      "host": "route.host.com",
      "path": "/ppp"
    }
    routesToAdd = []
    for x in range(0,5):
        #print(":" + str(x).strip() + ":")
        routesToAdd.append({
          "protocol": "http",
          "host": "route.host" + str(x).strip() + ".com",
          "path": "/ppp"
        })

    #delete service and it's routes if it exists
    self.deleteService(serviceName)

    serviceResp = self.createServiceAndRoute(serviceName, route)
    #print("serviceResp:", serviceResp)

    #Add Extra routes to the services
    for curroute in routesToAdd:
      postData = {
        "strip_path": False,
        "preserve_host": False,
        "service": {"id": serviceResp["serviceID"]},
        "protocols": [curroute["protocol"]],
        "hosts": [curroute["host"]],
        "paths": [curroute["path"]]
        #append_comma_seperated_value methods ${ROUTE_METHODS}
      }
      resp, respCode = self.callKongService("/routes", {}, "post", postData, [201])

    #Get list of routes for this service`
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),6,msg="Setup routes not right")

    #Call function
    cmdToExecute = "./scripts/kong_delete_all_routes_apart_from_one"
    cmdToExecute += " " + self.kong_server
    cmdToExecute += " " + serviceName
    cmdToExecute += " " + "INVALID_ROUTE_ID"
    expectedOutput = ""
    expectedOutput += "Start of ./scripts/kong_delete_all_routes_apart_from_one\n"
    expectedOutput += "Wrong number of arguments expected 3 - got 0\n"
    expectedOutput += "Recieved args:\n"
    expectedOutput += "['./scripts/kong_delete_all_routes_apart_from_one']\n-"
    expectedErrorOutput = None

    a = self.executeCommand(cmdToExecute, expectedOutput, expectedErrorOutput, [0], 1, True)


    #Check only the one route we wanted lasts
    resp, respCode = self.callKongService("/services/" + serviceName + "/routes", {}, "get", postData, [200])
    self.assertEqual(len(resp["data"]),0,msg="All routes should be deleted")
