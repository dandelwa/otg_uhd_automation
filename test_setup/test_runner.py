from os import system
import subprocess

class Tests() :
    def __init__(self, tests, path, logging, mode="systest",Timeout = 120, suite="BGP") :
        self.timeout = "120"
        self.no_of_tests = 0
        self.suite = suite
        self.test_to_run = None
        self.skeleton = ""
        self.tests = tests
        self.test_to_run = ""
        self.path = path
        self.logging = logging
    

    def get_test(self):
        if self.suite =="BGP":
            self.no_of_tests = len(self.tests["BGP"])
            self.test_to_run = self.tests["BGP"]
        elif self.suite == "ISIS":
            self.no_of_tests = len(self.tests["ISIS"])
            self.test_to_run = self.tests["ISIS"]
        elif self.suite == "ISIS_BGP":
            self.no_of_tests = len(self.tests["ISIS_BGP"])
            self.test_to_run = self.tests["ISIS_BGP"]
    

    
    def run_test(self):    
        for test in self.test_to_run:
            self.show_details(test)
            no_of_devices = self.test_to_run[test]["no_of_devices"]
            no_of_ports = self.test_to_run[test]["no_of_ports"]
            no_of_flows = self.test_to_run[test]["noofflows"]
            no_of_pkts = self.test_to_run[test]["noofpkts"]
            frame_size = self.test_to_run[test]["framesize"]
            cmd1 = "cd %s\n" % (self.path)
            cmd2 = "python3 -m pytest -k test_bgp.py --noofdevices %s --noofports %s --noofpkts %s --noofflows %s --framesize %s --sessiontimeout %s" \
                % (no_of_devices, no_of_ports, no_of_pkts, no_of_flows, frame_size, self.timeout)
            cmd = cmd1 + cmd2
            contents = subprocess.check_output(cmd, shell=True, text= True)
            print(contents)
            self.logging.info(contents)
    
    def show_details(self, index):
        self.logging.info("Running test for %s" % (self.suite))
        print("Running Test for %s" % (self.suite))
        self.logging.info("Running test with these arguments")
        self.logging.info(self.test_to_run[index])
        print(self.test_to_run[index])


            
