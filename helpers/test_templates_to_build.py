#!/usr/bin/env python

###
### Tests for templates to build
###

import unittest
from templates_to_build import templates_to_build

__author__     = "Luca Prete"
__copyright__  = "Copyright 2019"
__license__    = "AGPL3"
__maintainer__ = "Luca Prete"
__email__      = "lucaprete@teamdigitale.governo.it"
__status__     = "Development"

class TestFlatList(unittest.TestCase):
  def setUp(self):
      pass

  def test_empty_output(self):
    """If the list of file doesn't match any
    packer template expect an empty set
    """
    files_modified = [
      "will_never_work.yml",
      "ansible/roles/will_never_work"
    ]
    output = templates_to_build(files_modified)
    self.assertEqual(output, set())

  def test_exclude_dirs(self):
    """If the list of files contains folder
    dirs expect empty set
    """
    files_modified = [
      "helpers",
      "helpers/templates_to_build.py",
      ".circleci"
    ]

    output = templates_to_build(files_modified)
    self.assertEqual(output, set())

  def test_existing_template(self):
    """If the list of files matches an existing
    Packer template, expect the template in the
    set
    """
    files_modified = [
      "base.json"
    ]
    output = templates_to_build(files_modified)
    self.assertIn("base.json", output)

  def test_existing_playbook(self):
    """If the list of files matches an existing
    Ansible playbook, expect at least the base
    template in the set
    """
    files_modified = [
      "ansible/base.yml"
    ]
    output = templates_to_build(files_modified)
    self.assertIn("base.json", output)

  def test_existing_role(self):
    """If the list of files matches an existing
    Ansible role, expect at least the base template
    in the set
    """
    files_modified = [
      "ansible/roles/azure-deprovision"
    ]
    output = templates_to_build(files_modified)
    self.assertIn("base.json", output)

  def test_existing_role_subfiles(self):
    """If the list of files matches one or more
    existing Ansible role internal files, expect
    at least the base template in the set
    """
    files_modified = [
      "ansible/roles/azure-deprovision/tasks/main.yml",
      "ansible/roles/azure-deprovision/defaults/main.yml",
    ]
    output = templates_to_build(files_modified)
    self.assertIn("base.json", output)

    # TODO: Test role hinerited from different Packer
    # templates as soon as multiple templates are defined

if __name__ == '__main__':
  unittest.main()
