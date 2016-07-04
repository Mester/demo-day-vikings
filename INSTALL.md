# Instructions to get celery up and running

### I prefer to install the RabbitMQ broker (that is needed to run celery task workers) in a virtual machine. `vagrant` is the best way to get a virtual machine up and running in no time. 

### Follow the steps on `vagrantup.com` and get your vagrantbox up and running

### When you are done, run `vagrant ssh` to ssh into your vagrant machine. This should be done in the same directory where you had initialized the vagrant virtual machine. 

### You will now be in a ssh session inside the virtual machine. Run the following:

`sudo apt update && sudo apt upgrade --yes`
`sudo apt install rabbitmq-server`

### If you see the following: 
`Starting rabbitmq-server: SUCCESS`
### Then rabbitmq is up and running. 

### Find out the IP address of your virtual machine by running 
`ip addr show`

### You will see an output like:
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:92:18:9d brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe92:189d/64 scope link
       valid_lft forever preferred_lft forever
```

### Not the Ip Address. In the above example it is `10.0.2.15`

### Exit the ssh session by hittin Ctrl-D. Do not run `vagrant halt` or `vagrant destroy`. We want to keep the virtual machine running

### Once you quit the ssh session, and return the original directory on your host, open up the VagrantFile. Create if not already created.
`vim Vagrantfile`

### Add the following rule into that.
```
Vagrant.configure(2) do |config|
  config.vm.network "forwarded_port", guest: 5672, host: 5001
end
```

### There might be other config in your Vagrant.configure block, don't screw with them. Now rabbitmq-server, in our virtual machine, is running on port 5672. We have now forward port 5001 on our host to port 5672 on the virtual machine, as if rabbitmq is now running on port 5001

### Now it's time to restart the virtual machine, for the rules to take effect.Run the following commands from the same directory

```
vagrant halt && vagrant up
```

### Now open up `music_app.py/settings.py` and add the following configuration 
```
BROKER = "amqp://localhost:5001"
``` 

### Replace the IP address with the IP address of the virtual machine you found in the above step. Save and close `music_app/settings.py`

### Assuming that everything is working the way it should, you now start the celery worker using the following: (Run it in the root of the project)
```
celery -A tasks worker --loglevel=info
```

### Now run the server in some other terminal, you should see celery in action
```
python run_server.py
```
