import pytest

class Tests() :
    def __init__(self, tests,Timeout = 120, suite="BGP") :
        self.timeout = 120
        self.no_of_tests = 0
        self.suite = suite
        self.test_to_run = None
        self.skeleton = ""
        self.tests = tests
        self.test_to_run = ""
    
    def get_test(self):
        if self.suite =="BGP":
            self.no_of_tests = len(self.tests["BGP"])
            self.test_to_run = self.tests["BGP"]
    
    def run_test(self):    
        for test in self.test_to_run:
            skeleton = []
            if self.suite == "BGP":
                skeleton.append("test_bgp.py")
            no_of_devices = self.test_to_run[test]["no_of_devices"]
            no_of_ports = self.test_to_run[test]["no_of_ports"]
            no_of_flows = self.test_to_run[test]["noofflows"]
            no_of_pkts = self.test_to_run[test]["noofpkts"]
            frame_size = self.test_to_run[test]["framesize"]
            skeleton.append("--noofdevices")
            skeleton.append(no_of_devices)
            skeleton.append("--noofports")
            skeleton.append(no_of_ports)
            skeleton.append("--noofflows")
            skeleton.append(no_of_flows)
            skeleton.append("--noofpkts")
            skeleton.append(no_of_pkts)
            skeleton.append("--framesize")
            skeleton.append(frame_size)
            skeleton.append("--sessiontimeout")
            skeleton.append(self.timeout)
            result = pytest.main(skeleton)
            print(result)

            