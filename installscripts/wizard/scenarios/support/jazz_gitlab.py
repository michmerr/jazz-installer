#!/usr/bin/python
import os
import subprocess

from jazz_common import get_tfvars_file, replace_tfvars


def add_gitlab_config_to_files(parameter_list):
    """
    Add gitlab configuration to terraform.tfvars
    parameter_list = [  gitlab_public_ip ,
                        gitlab_username,
                        gitlab_passwd ]
    """
    print("Adding Gitlab config to Terraform variables")
    replace_tfvars('scm_publicip', parameter_list[0], get_tfvars_file())
    replace_tfvars('scm_elb', parameter_list[0], get_tfvars_file())
    replace_tfvars('scm_username', parameter_list[1], get_tfvars_file())
    replace_tfvars('scm_passwd', parameter_list[2], get_tfvars_file())
    replace_tfvars('scm_type', 'gitlab', get_tfvars_file())
    replace_tfvars('scm_pathext', '/', get_tfvars_file())


def get_and_add_docker_gitlab_config(gitlab_docker_path, parameter_cred_list=[]):
    """
        Launch a Dockerized Gitlab server.
    """
    os.chdir(gitlab_docker_path)
    print("Running docker launch script  for gitlab")

    subprocess.call([
        'sg', 'docker',  './launch_gitlab_docker.sh %s %s' %( str(parameter_cred_list[1]) , str(parameter_cred_list[0])), '|', 'tee', '-a',
        '../../gitlab_creation.out'
    ])

    print("Gitlab container launched")

    # Get values to create the array
    parameter_list = []
    with open("docker_gitlab_vars") as f:
        for line in f:
            parameter_list.append(line.rstrip())

    print(parameter_list[0:])

    add_gitlab_config_to_files(parameter_list)
