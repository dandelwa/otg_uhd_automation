import subprocess
import re

class deployment():
    def __init__(self, releaseinfourl, deploymentfilepath, historyfile):
        self.controller_version_to_be_deployed = ""
        self.gnmi_version_to_be_deployed = ""
        self.historyfile = historyfile
        self.current_deployed_version = self.read_data_from_history()
        self.release_info_url = releaseinfourl
        self.deployment_file = deploymentfilepath
        
    
    def read_data_from_history(self):
        history = open(self.historyfile, 'r')
        controller = history.readline()
        gnmi = history.readline()
        return {'controller':controller, 'gnmi' :gnmi}

    def get_latest_release(self):
        cmd = ' curl -s %s ' % (self.release_info_url)
        contents = subprocess.check_output(cmd, shell=True, text= True)
        contents = contents.split("\n")
        release = {}
        for line in contents:
            if "ixia-c-gnmi-server" in line:
                gnmi = line
                break
        pattern = r"\[(.*?)\]"

        match = re.search(pattern, gnmi)

        if match:
            version = match.group(1)
            self.gnmi_version_to_be_deployed = version
        else:
            print("No match found.")

        for line in contents:
            if "ixia-c-controller" in line:
                gnmi = line
                break
        pattern = r"\[(.*?)\]"

        match = re.search(pattern, gnmi)

        if match:
            version = match.group(1)
            self.controller_version_to_be_deployed = version

        return(release)
    
    def update_yaml_for_deployment(self):
        yaml_file_path = "%s/ixia-c-controller.yaml" % (self.deployment_file)
        yaml_file_path_modified = "%s/ixia-c-controller_deploy.yaml" % (self.deployment_file)
        yaml_file = open(yaml_file_path, "r")
        deploy_file = open(yaml_file_path_modified, "w")
        for line in yaml_file:
            if "<controller>" in line.strip():
                line = "          image: docker-virtual-p4isg.artifactorylbj.it.keysight.com/controller:%s\n" % (self.controller_version_to_be_deployed)
            elif "<gnmi>" in line.strip():
                line = "        - image: ghcr.io/open-traffic-generator/ixia-c-gnmi-server:%s\n" % (self.gnmi_version_to_be_deployed)
            deploy_file.write(line)
        return
    
    def deploy_yaml_file(self):
        self.update_yaml_for_deployment()
        cmd = "cd %s \n kubectl apply -f ixia-c-controller_deploy.yaml" % (self.deployment_file)
        contents = subprocess.check_output(cmd, shell=True, text= True)
        print(contents)
        updatehistory = open(self.historyfile, "w")
        self.current_deployed_version["gnmi"] = self.gnmi_version_to_be_deployed
        self.current_deployed_version["controller"] = self.controller_version_to_be_deployed
        updatehistory.write(self.controller_version_to_be_deployed+"\n"+self.gnmi_version_to_be_deployed)

    def current_controller_version(self):
        if self.current_deployed_version != {}:
            return (self.current_deployed_version['controller'])
        else:
            return "No Deployment performed. Run deployment to have this info available."
        
    def current_gnmi_version(self):
        if self.current_deployed_version != {}:
            return (self.current_deployed_version['gnmi'])
        else:
            return "No Deployment performed. Run deployment to have this info available."
    
    def latest_availabe_release(self):
        current_release = "Controller %s | GNMI %s" % (self.controller_version, self.gnmi_version)
        return current_release