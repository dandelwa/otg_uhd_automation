from deployment.deploy import deployment
from setup_const  import *
import logging
from test_setup.test_runner import Tests
from test_setup.test_to_run import tests

logging.basicConfig(filename=MAINLOGFILE, filemode='w', format='%(name)s - %(levelname)s - %(message)s',  level=logging.DEBUG)
#first lets write a code that will ensure the latest setup is ready.
#get_release and then deploy controller on target box. this must run in same machine where one is running 
#the deploying the controller.

logging.info("Creating deployment class using releaseinfourl=%s and deploymentfilepath=%s" % (RELEASEINFOURL, DEPLOYMENTFILEPATH))
deploy = deployment(releaseinfourl=RELEASEINFOURL, deploymentfilepath=DEPLOYMENTFILEPATH, historyfile=HISTORYFILE)
logging.info("Object created for deployment : %s" % (deploy))
logging.info("Current versions are. Controller: %s and Gnmi : %s" % (deploy.current_controller_version(), deploy.current_gnmi_version()))

deploy.get_latest_release()
logging.info("Latest Controller version is %s  and gnmi version is %s" % (deploy.controller_version_to_be_deployed, deploy.gnmi_version_to_be_deployed))

if deploy.current_controller_version() != deploy.controller_version_to_be_deployed:
    deploy.deploy_yaml_file()

bgp_tests = Tests(tests, SYSTEMTESTPATH)
bgp_tests.get_test()
bgp_tests.run_test()
