#!/usr/bin/env python

###
### Templates to build
###
### Returns the list of Packer templates to rebuild
### from the list of files modified in the repository
### at each commit. Then build the templates using Packer.
###

import subprocess
from sys import exit

__author__     = "Luca Prete"
__copyright__  = "Copyright 2019"
__license__    = "AGPL3"
__maintainer__ = "Luca Prete"
__email__      = "lucaprete@teamdigitale.governo.it"
__status__     = "Development"

def run_command(command):
  """Runs the command specified and returns the output
  in form of a list
  
  command  -- the command to execute
  """
  proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  return filter(None, out.rstrip().split("\n"))

def run_command_stream(command):
  """Runs the command specified and streams the output.
  Once finished, it returns the exit code.
  
  command  -- the command to execute
  """
  process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)

  while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
          break
      if output:
          print output.strip()

  return process.poll()

def grep_in_path(value):
  """Returns the list of files containing the value
  specified, excluding the .git and the helpers directories
  
  value  -- the value to look for
  """
  return run_command("grep -l -R --exclude-dir='.git' --exclude-dir='helpers' %s ." % (value))

def build(templates_to_build):
  """Invokes Packer to build the templates given in input

  templates_to_build  -- the list of Packer templates to rebuild
  """
  if len(templates_to_build) == 0:
    print("None of the images requires to be built.")
    return

  for template in templates_to_build:
    print("Building image for template: %s. This may take several minutes..."  % (template))
    rc = run_command_stream("packer build -force %s" % template)
    if rc != 0:
      exit("Something went wrong. Template %s wasn't built successfully." % template)

def templates_to_build(list_of_files):
  """Returns the list of Packer templates to rebuild
  
  list_of_files  -- the list of files modified
  """
  templates_to_build = set()

  for file_path_name in list_of_files:
    # If the helpers or .circleci are in the path continue
    if "helpers" in file_path_name or ".circleci" in file_path_name:
      continue

    # If the file has a json extension it's a Packer template.
    # Add it to the set of templates to build.
    if ".json" in file_path_name:
      file_name = file_path_name.split("/")[-1]
      templates_to_build.add(file_name)

    # If the roles directory is in the file path it's an
    # Ansible role. Get the role name, look what Ansible
    # playbook uses it. Then, look what Packer template
    # uses it and add it to the set of templates to rebuild
    elif "/roles/" in file_path_name:
      role = file_path_name.split("/")[2]
      for playbook_path in grep_in_path(role):
        playbook = playbook_path.split("/")[-1]
        for template in grep_in_path(playbook):
          templates_to_build.add(template.split("/")[-1])

    # If the roles directory is not in the path and the file
    # extension is yml it's an Ansible playbook. look what
    # Packer template uses it and add it to the set of templates
    # to rebuild
    elif ".yml" in file_path_name:
      for template in grep_in_path(file_path_name):
        templates_to_build.add(template.split("/")[-1])

  return templates_to_build

def main():
  """Retrieves the list of files modified in the current repository
  during the last commit and prints the list of Packer templates
  affected by the change. Then, it builds the images needed invoking
  Packer.
  """
  files_modified = run_command("git diff-tree --no-commit-id --name-only -r HEAD")
  templates = templates_to_build(files_modified)
  build(templates)

if __name__ == "__main__":
  main()
