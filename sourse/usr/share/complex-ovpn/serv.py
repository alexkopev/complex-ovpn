#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, time
import os, shutil
from zipfile import ZipFile

def main():
    try:
        os.mkdir("/etc/openvpn/log")
    except OSError:
        pass
    try:
        os.mkdir("/etc/openvpn/ccd")
    except OSError:
        pass
    proj_folder = os.path.abspath(os.curdir)
    key_dir = "export KEY_DIR="
    f_read = open("/etc/openvpn/easy-rsa/vars").readlines()
    f_write = open("/etc/openvpn/easy-rsa/vars", "w")
    for string in f_read:
        if string.find(key_dir) != -1:
            string = "export KEY_DIR=\"/etc/openvpn/keys\"""\n"
        f_write.write(string)
    f_write.close()
    os.chdir('/etc/openvpn/easy-rsa')
    os.system ("sudo sh -c '. ./vars && ./clean-all && ./pkitool --initca && ./build-dh && ./pkitool --server openvpn_server'")
    os.remove("/etc/openvpn/keys/openvpn_server.csr")
    os.chdir(proj_folder)

def get_param_serv(country, province, city, ou, org, email):
    try:
        shutil.copytree('/usr/share/easy-rsa', '/etc/openvpn/easy-rsa/')
    except OSError:
        pass
    key_country = "export KEY_COUNTRY=\""
    key_province = "export KEY_PROVINCE=\""
    key_city = "export KEY_CITY=\""
    key_ou = "export KEY_OU=\""
    key_org = "export KEY_ORG=\""
    key_email = "export KEY_EMAIL=\""
    f_read = open("/etc/openvpn/easy-rsa/vars").readlines()
    f_write = open("/etc/openvpn/easy-rsa/vars", "w")
    for string in f_read:
        if string.find(key_country) != -1:
            string = key_country + country + "\"\n"
        if string.find(key_province) != -1:
            string = key_province + province + "\"\n"
        if string.find(key_city) != -1:
            string = key_city + city + "\"\n"
        if string.find(key_ou) != -1:
            string = key_ou + ou + "\"\n"
        if string.find(key_org) != -1:
            string = key_org + org + "\"\n"
        if string.find(key_email) != -1:
            string = key_email + email + "\"\n"
        f_write.write(string)
    f_write.close()

def set_param_serv():
    try:
        shutil.copytree('/usr/share/easy-rsa', '/etc/openvpn/easy-rsa/')
    except OSError:
        pass
    key_country = "export KEY_COUNTRY=\""
    key_province = "export KEY_PROVINCE=\""
    key_city = "export KEY_CITY=\""
    key_ou = "export KEY_OU=\""
    key_org = "export KEY_ORG=\""
    key_email = "export KEY_EMAIL=\""
    f_read = open("/etc/openvpn/easy-rsa/vars").readlines() 
    for string in f_read:
        if string.find(key_country + "US\"") != -1:
            return 1
            break
        if string.find(key_country) != -1:
            nach_key_country = string.find("\"")
            kon_key_country = string.rfind("\"")
            country = string [nach_key_country + 1 : kon_key_country]
        if string.find(key_province) != -1:
            nach_key_province = string.find("\"")
            kon_key_province = string.rfind("\"")
            province = string [nach_key_province + 1 : kon_key_province]
        if string.find(key_city) != -1:
            nach_key_city = string.find("\"")
            kon_key_city = string.rfind("\"")
            city = string [nach_key_city + 1 : kon_key_city]
        if string.find(key_ou) != -1:
            nach_key_ou = string.find("\"")
            kon_key_ou = string.rfind("\"")
            ou = string [nach_key_ou + 1 : kon_key_ou]
        if string.find(key_org) != -1:
            nach_key_org = string.find("\"")
            kon_key_org = string.rfind("\"")
            org = string [nach_key_org + 1 : kon_key_org]
        if string.find(key_email) != -1:
            nach_key_email = string.find("\"")
            kon_key_email = string.rfind("\"")
            email = string [nach_key_email + 1 : kon_key_email]
    return (country, province, city, ou, org, email)
            
def new_client(client_name):
    proj_folder = os.path.abspath(os.curdir)
    os.chdir('/etc/openvpn/easy-rsa')
    lists = pars_all_clients()
    if client_name in lists:
        os.chdir(proj_folder)
        return (1)
    else:
        os.system ("sudo sh -c '. ./vars && ./pkitool '"+ client_name)
        shutil.move('/etc/openvpn/keys/'+client_name+'.key', '/etc/openvpn/ccd/')
        shutil.move('/etc/openvpn/keys/'+client_name+'.crt', '/etc/openvpn/ccd/')
        os.remove('/etc/openvpn/keys/'+client_name+'.csr')
        os.chdir(proj_folder)

    
def pars_all_clients():
    lists = []
    f_read = open("/etc/openvpn/keys/index.txt").readlines()
    for string in f_read:
        if string[0] == "V":
            nach = string.find("/CN=")
            kon = string.find("/name")
            lists.append (string[nach+4:kon])
    return (lists)

def revoke_cert(client_name):
    proj_folder = os.path.abspath(os.curdir)
    os.chdir('/etc/openvpn/easy-rsa')
    os.system ("sudo sh -c '. ./vars && ./revoke-full /etc/openvpn/ccd/'"+ client_name)
    os.remove ('/etc/openvpn/ccd/'+client_name+'.crt')
    os.remove ('/etc/openvpn/ccd/'+client_name+'.key')
    os.chdir(proj_folder)

def server_config_file(port, proto, ip = 0, mask = 0):
    serv_config = []
    serv_config.append('port ' + port)
    serv_config.append('proto ' + proto)
    serv_config.append('dev tap')
    serv_config.append('ca /etc/openvpn/keys/ca.crt')
    serv_config.append('cert /etc/openvpn/keys/openvpn_server.crt')
    serv_config.append('key /etc/openvpn/keys/openvpn_server.key')
    serv_config.append('dh /etc/openvpn/keys/dh2048.pem')
    serv_config.append('server 10.8.0.0 255.255.255.0')
    serv_config.append('client-config-dir /etc/openvpn/ccd')
    serv_config.append('ifconfig-pool-persist ipp.txt')
    if ip and mask:
        serv_config.append('push "route ' + ip + ' ' + mask + "\"")
    serv_config.append('keepalive 10 120')
    serv_config.append('management localhost 7777')
    serv_config.append('comp-lzo')
    serv_config.append('user nobody')
    serv_config.append('group nogroup')
    serv_config.append('persist-key')
    serv_config.append('persist-tun')
    serv_config.append('log /etc/openvpn/log/openvpn.log')
    serv_config.append('status /etc/openvpn/log/openvpn-status.log')
    serv_config.append('verb 3')
    return (serv_config)

def template_client_config (out_ip, port, proto):
    client_config = []
    client_config.append('client')
    client_config.append('remote '+ out_ip + ' ' + port)
    client_config.append('proto ' + proto)
    client_config.append('dev tap')
    client_config.append('ca ca.crt')
    client_config.append('cert client_name.crt')
    client_config.append('key client_name.key')
    client_config.append('keepalive 10 120')
    client_config.append('comp-lzo')
    client_config.append('user nobody')
    client_config.append('group nogroup')
    client_config.append('persist-key')
    client_config.append('persist-tun')
    client_config.append('log openvpn.log')
    client_config.append('verb 3')
    f = open("/etc/openvpn/ccd/openvpn_client.conf", "w")
    for line in client_config:
        print(line, file = f)
    f.close()

def write_conf_serv (lists, out_ip, port, proto):
    f = open('/etc/openvpn/openvpn_server.conf', "w")
    for line in lists:
        print(line, file = f)
    f.close()
    template_client_config (out_ip, port, proto)

def save_client_conf(client_name): # подготовка конфигурационных файлов клиента для сохранения
    lists = pars_all_clients()
    lists.pop (0)
    if client_name in lists:
        try: 
            os.mkdir('/etc/openvpn/ccd/'+client_name)
        except:
            shutil.rmtree('/etc/openvpn/ccd/'+client_name)
            os.mkdir('/etc/openvpn/ccd/'+client_name)
        shutil.copy('/etc/openvpn/ccd/openvpn_client.conf', '/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf')
        f_read = open('/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf').readlines()
        f_write = open('/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf', "w")
        for string in f_read:
            if string.find("client_name") != -1:
                string = string.replace("client_name", client_name)
            f_write.write(string)
        f_write.close()
        shutil.copy('/etc/openvpn/keys/ca.crt', '/etc/openvpn/ccd/'+client_name+'/ca.crt')
        shutil.copy('/etc/openvpn/ccd/'+client_name+'.crt', '/etc/openvpn/ccd/'+client_name+'/'+client_name+'.crt')
        shutil.copy('/etc/openvpn/ccd/'+client_name+'.key', '/etc/openvpn/ccd/'+client_name+'/'+client_name+'.key')
    else:
        return (1)

def Windows_client_conf (client_name):
    f_read = open('/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf').readlines()
    f_write = open('/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf', "w")
    for string in f_read:
        string_new = string + "\r\n"
        if string.find("user nobody") != -1:
            string_new = string.replace("user nobody\n", "")
        if string.find("group nogroup") != -1:
            string_new = string.replace("group nogroup\n", "")
        f_write.write(string_new)
    f_write.close()
    os.rename('/etc/openvpn/ccd/'+client_name+'/openvpn_client.conf','/etc/openvpn/ccd/'+client_name+'/openvpn_client.ovpn')

def archive_client_conf(client_name):
    proj_folder = os.path.abspath(os.curdir)
    os.chdir('/etc/openvpn/ccd/'+client_name)
    z = ZipFile(client_name + '.zip', 'w')
    dir_client_conf = os.listdir ('/etc/openvpn/ccd/'+client_name)
    dir_client_conf.remove(client_name + '.zip')
    for file_list in dir_client_conf:
        z.write(file_list)
    z.close()
    os.chdir(proj_folder)

def archive_client_conf_save_in(client_name, folder):
    if os.path.exists(folder + '/' + client_name + '.zip') == True:
        file_name = folder + '/' + client_name + " " + time.asctime() + '.zip'
        shutil.copy('/etc/openvpn/ccd/'+ client_name + '/' + client_name + '.zip', file_name)
    else:
        file_name = folder + '/' + client_name + '.zip'
        shutil.copy('/etc/openvpn/ccd/'+ client_name + '/' + client_name + '.zip', file_name)
    os.system ('chmod 666 "' + file_name + '"')

if __name__ == '__main__':
    main()
