#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from netmiko import Netmiko
from getpass import getpass
from datetime import datetime
from utils.out import *
import config
import os
import sys
import time

# Paramètres password & time
pass_all = getpass()
now_uptime = datetime.now()
date_uptime = now_uptime.strftime("%d_%m_%Y_%H:%M:%S")

def banner():
    cisco_automation = """\033[92m
 ____ _                    _         _                        _   _
 / ___(_)___  ___ ___      / \  _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __
| |   | / __|/ __/ _ \    / _ \| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \
| |___| \__ \ (_| (_) |  / ___ \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |
 \____|_|___/\___\___/  /_/   \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
 \033[0m"""
    return cisco_automation

# Paramètres de connexion netmiko
def get_dic(ip):
    dic_only = {
        "ip": ip,
        "username": config.user,
        "password": pass_all,
        "device_type": config.cisco_type,
        #"secret": root,
    }
    return dic_only

# Fin de tâche + execution time
def end_task():
    print("[Execution time : {0} seconds]".format(round(time.time() - start_time)))
    sys.exit()

# Récupération du hostname
def get_hostname():
    sh_check = net_connect.send_command("show run | in hostname")
    hostname = sh_check.split()
    return hostname[1]

# Attente de l'attribution de l'IP + récupération de cette dernière
def get_ip_dhcp(ip):
    show_info("Waiting DHCP ACK...")
    # Attente de l'ip avant de continuer
    time.sleep(12)
    net_connect = Netmiko(**get_dic(ip))
    net_connect.enable()
    dhcp_check = net_connect.send_command("sh ip int brief | in DHCP")
    dhcp = dhcp_check.split()
    return dhcp[1]

# Création des dossiers de backup avec l'hostname
def create_all_files(ip_address):
    path_backup = "backups/{0}".format(get_hostname())
    # droits d'accès
    rights = 0o755
    if not os.path.isdir(path_backup):
        os.mkdir(path_backup, rights)

# Backup toutes les config au format .txt
def backup_configs():
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H:%M:%S")
    path_backup = "backups/{0}/{1}.txt".format(get_hostname(),date)
    conf = net_connect.send_command("sh run")
    show_result(path_backup)
    # Sauvegarde de la configuration dans backup/hostname
    with open(path_backup, "a") as file:
        file.write(conf + "\n")

# Désactive le enable pass et active le secret
def enable_md5():
    enable = net_connect.send_command("sh run | include enable")
    check = enable.split()
    # Vérification de l'enable password
    if check[1] == "password":
        pass_type5 = getpass(show_input('Choose a strong password : '))
        enable = ['no enable password', 'enable secret %s' % (pass_type5)]
        conf_t = net_connect.send_config_set(enable)
        show_info("enable secret activated")
        # Demande de write la conf
        save = input(show_input("Do you want to write configuration ? (y/n) : "))
        if save == "y" or save == "yes":
            write_conf(ip)
    else:
        show_info("enable secret is already activated !")

# Récupération ip route
def ip_route():
    route = net_connect.send_command("sh ip int br")
    show_result(route)

# Listing des clients DHCP
def dhcp_binding():
    binding = net_connect.send_command("sh ip dhcp binding")
    show_result(binding)

# Vérification de l'environment
def get_environment():
    measured = net_connect.send_command("sh environment")
    all = net_connect.send_command("sh environment all | in measured")
    show_result(measured)
    print(all)

# Sauvegarde la configuration
def write_conf(ip):
    net_connect = Netmiko(**get_dic(ip))
    net_connect.enable()
    net_connect.save_config()
    show_result("configuration saved")

# Récupération de la version
def get_version():
    version = net_connect.send_command("show version | in IOS")
    show_result(version)

# Configure un pool DHCP sur la cible
def dhcp_pool(ip):
    try:
        show_result("Reading dhcp_pool file...")
        net_connect = Netmiko(**get_dic(ip))
        print("-------------------------------------------------")
        net_connect.enable()
        # Envoie la configuration du fichier dhcp_pool
        net_connect.send_config_from_file("dhcp_pool")
        show_result("DHCP pool configured !")
        # Demande de write la conf
        save = input(show_input("Do you want to write configuration ? (y/n) : "))
        if save == "y" or save == "yes":
            write_conf(ip)
        end_task()
        print("-------------------------------------------------")
    except:
        show_info("host [{0}] unreachable".format(ip_address))
        end_task()

# Configuration de l'interface ciblée en DHCP
def dhcp_client(ip):
    try:
        interface = input(show_input("Specify target interface : "))
        net_connect = Netmiko(**get_dic(ip))
        print("-------------------------------------------------")
        net_connect.enable()
        enable = [interface, 'ip address dhcp', 'no sh']
        conf_t = net_connect.send_config_set(enable)
        print(conf_t)
        print("-------------------------------------------------")
        # Affiche l'IP reçue par le DHCP
        show_result("You got {0} from DHCP".format(get_ip_dhcp(ip)))
        # Demande de write la conf
        save = input(show_input("Do you want to write configuration ? (y/n) : "))
        if save == "y" or save == "yes":
            write_conf(ip)
        end_task()
        print("-------------------------------------------------")
    except:
        show_info("host [{0}] unreachable".format(ip_address))
        end_task()

# uptime + stocke dans un fichier .txt dans le dossier results
def uptime():
    path_uptime = "results/{0}.txt".format(date_uptime)
    uptime = net_connect.send_command("show version | in uptime")
    show_result(uptime)
    with open(path_uptime, "a") as file:
        file.write(uptime + "\n")

# Affichage du menu
def menu():
    print (banner() + """\033[96m
 [*] Manage your switches & routers [*]

   [1]--Check Uptime on all devices
   [2]--Backup all configuration
   [3]--Enable secret & disable low security
   [4]--Check IP Route
   [5]--Check DHCP Binding
   [6]--Setup DHCP client on interface
   [7]--Setup DHCP Pool
   [8]--Check environment
   [9]--Get version
   [0]--Exit
   \033[0m
 """)

menu()
choice = input(show_cisco())
start_time = time.time()

#Pour les options 6 & 7 pas de d'utilisation de router.list
if choice == "6":
    ip = input(show_input("Specify target IP : "))
    dhcp_client(ip)
elif choice == "7":
    ip = input(show_input("Specify target IP : "))
    dhcp_pool(ip)
elif choice == "0":
    os.system('clear'), sys.exit()
elif choice == "":
    menu()

# Boucle sur les cibles présentes dans router.list
for line in config.router_list:
    ip_address = line.strip()
    # Paramètres netmiko pour l'utilisation de router.list
    dic = {
        "ip": ip_address,
        "username": config.user,
        "password": pass_all,
        "device_type": config.cisco_type,
        #"secret": root,
    }
    try:
        net_connect = Netmiko(**dic)
        # Affichage du hostname de la cible
        print("Connected successfully to {0}".format(get_hostname()))
        print("-------------------------------------------------")
        net_connect.enable()
        # Choix d'options
        if choice == "1":
            uptime()
        elif choice == "2":
            create_all_files(ip_address)
            backup_configs()
        elif choice == "3":
            enable_md5()
        elif choice == "4":
            ip_route()
        elif choice == "5":
            dhcp_binding()
        elif choice == "8":
            get_environment()
        elif choice == "9":
            get_version()
        print("-------------------------------------------------")
    except:
        show_info("host [{0}] unreachable".format(ip_address))
        continue
    # Déconnexion netmiko
    net_connect.disconnect()

# Temps d'éxécution de la tâche
print("[Execution time : {0} seconds]".format(round(time.time() - start_time)))