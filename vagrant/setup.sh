#!/bin/bash

echo "Updating apt sources."
sudo apt-get update -qq

echo "Installing Python and build dependencies."
sudo apt-get install -y -qq python-dev python-pip python-virtualenv
sudo apt-get install -y -qq git build-essential

echo "Upgrading pip and installing pyperf."
sudo pip install -q -U pip
sudo pip install -q -U setuptools
sudo pip install -q -e /home/vagrant/pyperf

echo "Installing RabbitMQ"
sudo apt-get install rabbitmq-server

echo "Installing ZeroVM."
sudo su -c 'echo "deb http://packages.zerovm.org/apt/ubuntu/ precise main" > /etc/apt/sources.list.d/zerovm-precise.list'
wget -O- http://packages.zerovm.org/apt/ubuntu/zerovm.pkg.key | sudo apt-key add -
sudo apt-get update -qq
sudo apt-get install -y -qq zerovm*

echo "Installing LXC."
sudo apt-get install -y -qq lxc

echo "VM setup complete."
