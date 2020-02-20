![Python 3.6](https://img.shields.io/badge/python-3.6%2B-green)
![Netmiko 3.0.0](https://img.shields.io/badge/netmiko-3.0.0-yellow)
![cisco](https://img.shields.io/badge/cisco-ios-yellowgreen)


# Cisco-Automation

Cet outil a pour but d'**automatiser certaines tâches sur des équipements cisco**.

## Pré-requis

Vous aurez besoin d'un accès **SSH** sur les cibles, ainsi que d'un **même user** sur chacun d'entre eux.

## Installation

```bash
chmod +x main.py
pip3 install -r requirements.txt
```

## Configuration

Vous devez **renseigner l'username** dans la variable **user** du fichier **config.py** : 

![user](https://zupimages.net/up/20/08/hzyd.png)

Toute les **options** sauf l'option de création d'un **DHCP Pool** et du paramétrage d'une **interface en DHCP** s'éxécuteront sur les équipements présents dans le fichier **router.list**.

Ces deux fichiers sont à configurer **avant éxécution en fonction de vos besoins**.

Exemple **router.list** :
```bash
192.168.1.1
192.168.1.2
192.168.1.3
192.168.1.4
192.168.1.5
```

Exemple **dhcp_pool** :
```bash
ip dhcp pool NAME_POOL
network 192.168.1.0 255.255.255.0
dns-server 8.8.8.8
default-router 192.168.0.1
exit
ip dhcp excluded-address 192.168.1.1 192.168.1.10
```

## Usage

```bash
python3 main.py
```
![Menu](https://zupimages.net/up/20/08/qxq9.png)

## Quelques exemples

**Topologie** de test sur **GNS3** afin de **simuler plusieurs équipements** très simplement :

![GNS3](https://zupimages.net/up/20/08/ajrj.png)

 - **Backup des configuration** :
 
**Les backups sont sauvegardés au format txt dans le dossier backups :**

 ![config](https://zupimages.net/up/20/08/ugsm.png)
 
 - **Configuration d'une interface en DHCP** :
 
 Pour notre exemple, notre routeur est **connecté au NAT de GNS3** et son **interface** n'est **pas configurée** :
 
 ![nat](https://zupimages.net/up/20/08/ipoe.png)
 
 Nous devons donc renseigner le **routeur cible** qui est **R1** et son **interface** à qui nous souhaitons attribuer une **adresse IP** grâce au **DHCP** du **NAT**.
 
 ![dhcp](https://zupimages.net/up/20/08/q69s.png)
 
 Notre **routeur** se voit correctement assigné l'**adresse IP** :
 
 ![ip](https://zupimages.net/up/20/08/6ref.png)
 
 
   - **Check uptime** :
   
 **Les uptimes sont sauvegardés au format txt dans le dossier results :**
 
 ![config](https://zupimages.net/up/20/08/nyhp.png)
 
 - **Vérification de la température** :
 
 ![temp](https://zupimages.net/up/20/08/nmwy.png)
   

## Licence
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

