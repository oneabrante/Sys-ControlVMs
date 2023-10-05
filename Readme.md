<h2 style="text-align:center;"> Sys-ControlVMs - Virtual machines management with libvirt </h2>

<h4 style="text-align:center;">v1.0</h4> 
<p align="center"><img src="./viewer-flow/v1.0.gif" alt="Flow-v1.0" style="max-width:100%"></p>

<hr>

<h4 style="text-align:center;">v2.0</h4>
<p align="center"><img src="./viewer-flow/v2.0.gif" alt="Flow-v2.0" style="max-width:100%"></p>

<hr>

Obs:
This management needs a virbr0 interface, if you don't have it, you can start it with the following command:
    <br>
```bash
sudo virsh net-define /etc/libvirt/qemu/networks/autostart/default.xml
sudo virsh net-start default
```
    