from copy import copy

from edge_sim_py import *
import networkx as nx
import msgpack
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def first_fit(parameters):
    for service in Service.all():
        if service.server == None and not service.being_provisioned:

            for edge_server in EdgeServer.all():

                if edge_server.has_capacity_to_host(service=service):
                    service.provision(target_server=edge_server)
                    print("alloc")

                    break


def roundrobin(parameters):
    edge_servers = EdgeServer.all()
    count = 0
    for service in Service.all():

        while True:
            if service.server == None and not service.being_provisioned:

                edge_server = copy(edge_servers[count])

                if edge_server.has_capacity_to_host(service=service):
                    service.provision(target_server=edge_server)
                    print("alloc")
                    count += 1
                    print(count)

                    break
                if count == len(edge_servers):
                    count = 0
            break


def stopping_criterion(model: object):
    # Defining a variable that will help us to count the number of services successfully provisioned within the infrastructure
    provisioned_services = 0

    # Iterating over the list of services to count the number of services provisioned within the infrastructure
    for service in Service.all():

        # Initially, services are not hosted by any server (i.e., their "server" attribute is None).
        # Once that value changes, we know that it has been successfully provisioned inside an edge server.
        if service.server != None:
            provisioned_services += 1

    # As EdgeSimPy will halt the simulation whenever this function returns True, its output will be a boolean expression
    # that checks if the number of provisioned services equals to the number of services spawned in our simulation
    return provisioned_services == Service.count()

def run_simulation(algorithm):
    # Creating a Simulator object
    simulator = Simulator(
        tick_duration=1,
        tick_unit="seconds",
        stopping_criterion=stopping_criterion,
        resource_management_algorithm=algorithm,
    )

    # Loading a sample dataset from GitHub
    simulator.initialize(
        input_file="https://raw.githubusercontent.com/EdgeSimPy/edgesimpy-tutorials/master/datasets/sample_dataset2.json")

    # Executing the simulation
    simulator.run_model()


    # Checking the placement output
    print("Numero de servicos: " + str(Service.count()))
    for service in Service.all():
        print(f"{service}. Host: {service.server}")


def get_data():
    # Gathering the list of msgpack files in the current directory
    logs_directory = f"{os.getcwd()}/logs"
    dataset_files = [file for file in os.listdir(logs_directory) if ".msgpack" in file]

    # Reading msgpack files found
    datasets = {}
    for file in dataset_files:
        with open(f"logs/{file}", "rb") as data_file:
            datasets[file.replace(".msgpack", "")] = pd.DataFrame(
                msgpack.unpackb(data_file.read(), strict_map_key=False))
    return datasets


def get_edge_server_data(data):
    properties = ['Coordinates', 'CPU', 'CPU Demand', 'RAM', 'RAM Demand', 'Disk Demand', 'Services']
    columns = ['Time Step', 'Instance ID'] + properties
    dataframe = data["EdgeServer"].filter(items=columns)
    return dataframe


def test_algorithm(algorithm, algorithm_name):
    run_simulation(roundrobin)
    data = get_data()
    data_edge_server = get_edge_server_data(data)
    print(data_edge_server)
    data_edge_server.to_excel(algorithm_name + ".xlsx", index=False)


test_algorithm(first_fit, "first_fit")
test_algorithm(roundrobin, "roundrobin")
