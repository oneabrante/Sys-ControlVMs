import libvirt
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import turtle

#   Sys-ControlVMs - VMs management with libvirt
#   
#   S-CVMsv2.py - Script para o funcionamento do Sys-ControlVMs
#   
#
#   Website:        github.com/abrantedevops
#   Autor:          Thiago Abrante
#   Manutenção:     Thiago Abrante
#
# -----------------------------------------------------------------------------
#
#   COMO POSSO UTILIZAR ?
#   Este script pode ser chamado de maneira normal usando python3 e com o sudo 
#
#   Exemplo:
#   $ sudo python3 S-CVMsv2.py
#
# -----------------------------------------------------------------------------
#
#   ChangeLog:
#
#   v2.0 04/10/2023, Thiago Abrante
#     - Segunda versão!
#
# -----------------------------------------------------------------------------
#
#   Testado em:
#
#   Python 3.8.10
#   Linux Ubuntu 20.04 LTS
#
# -----------------------------------------------------------------------------
#

def gui():

    def connect_to_libvirt():
        try:
            conn = libvirt.open()
            if conn is None:
                print('Falha ao conectar à libvirt.')
                sys.exit(1)
            return conn
        except libvirt.libvirtError as e:
            print(f'Erro ao conectar à libvirt: {e}')
            sys.exit(1)

    def list_vms(conn):
        try:
            domains = conn.listAllDomains()
            if not domains:
                print('Nenhuma VM encontrada.')
            else:
                print('VMs disponíveis:')
                for domain in domains:
                    state, _ = domain.state()
                    state_str = "Desligada" if state == libvirt.VIR_DOMAIN_SHUTOFF else "Ligada"
                    print(f'Nome: {domain.name()} - Estado: {state_str}')
                    os.system('clear')
        except libvirt.libvirtError as e:
            print(f'Erro ao listar VMs: {e}')
        

    def start_vm(conn, vm_name):
        os.system('clear')
        try:
            domains = conn.listAllDomains()
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return
            domain = conn.lookupByName(vm_name)
            if domain.isActive():
                print(f'A VM {vm_name} já está ligada.')
            else:
                domain.create()
                print(f'A VM {vm_name} foi ligada.')
        except libvirt.libvirtError as e:
            print(f'Erro ao ligar VM {vm_name}: {e}')

    def stop_vm(conn, vm_name):
        os.system('clear')
        try:
            domains = conn.listAllDomains()
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return
            domain = conn.lookupByName(vm_name)
            if not domain.isActive():
                print(f'A VM {vm_name} já está desligada.')
            else:
                domain.destroy()
                print(f'A VM {vm_name} foi desligada.')
        except libvirt.libvirtError as e:
            print(f'Erro ao desligar VM {vm_name}: {e}')

    
    def create_vm_action():
        def back():
            labels_frame.destroy()
            root.destroy()

        conn = connect_to_libvirt()

        root = tk.Tk()
        root.title("Criar Máquina Virtual")
        root.geometry("490x370")

        labels_frame = ttk.LabelFrame(root, text="Preencha os campos abaixo para criar uma VM")
        labels_frame.grid(row=0, column=0, padx=10, pady=10)

        vm_name_label = ttk.Label(labels_frame, text="Nome da VM:")
        vm_name_label.grid(row=0, column=0, padx=10, pady=10)

        vm_name_entry = ttk.Entry(labels_frame)
        vm_name_entry.grid(row=0, column=1, padx=10, pady=10)

        disk_size_label = ttk.Label(labels_frame, text="Tamanho do disco (GB):")
        disk_size_label.grid(row=1, column=0, padx=10, pady=10)

        disk_size_entry = ttk.Entry(labels_frame)
        disk_size_entry.grid(row=1, column=1, padx=10, pady=10)

        memory_size_label = ttk.Label(labels_frame, text="Tamanho da memória (MiB):")
        memory_size_label.grid(row=2, column=0, padx=10, pady=10)

        memory_size_entry = ttk.Entry(labels_frame)
        memory_size_entry.grid(row=2, column=1, padx=10, pady=10)

        iso_choice_label = ttk.Label(labels_frame, text="Nome da imagem ISO:")
        iso_choice_label.grid(row=3, column=0, padx=10, pady=10)

        iso_choice_entry = ttk.Entry(labels_frame)
        iso_choice_entry.grid(row=3, column=1, padx=10, pady=10)

        os_choice_label = ttk.Label(labels_frame, text="Escolha do tipo de sistema operacional:")
        os_choice_label.grid(row=4, column=0, padx=10, pady=10)

        os_choice_entry = ttk.Entry(labels_frame)
        os_choice_entry.grid(row=4, column=1, padx=10, pady=10)

        network_choice_label = ttk.Label(labels_frame, text="Interface de rede padrão:")
        network_choice_label.grid(row=5, column=0, padx=10, pady=10)

        network_choice_entry = ttk.Entry(labels_frame)
        network_choice_entry.insert(0, "virbr0")
        network_choice_entry.configure(state='readonly')
        network_choice_entry.grid(row=5, column=1, padx=10, pady=10)
        
        create_vm_button = ttk.Button(labels_frame, text="Criar VM", command=lambda: create_vm(conn, vm_name_entry.get(), disk_size_entry.get(), memory_size_entry.get(), iso_choice_entry.get(), os_choice_entry.get(), network_choice_entry.get()))

        create_vm_button.grid(row=7, column=0, padx=(0,5), pady=30)

        back_button = ttk.Button(labels_frame, text="Voltar", command=back)
        back_button.grid(row=7, column=1, padx=(5,0), pady=30)

        root.mainloop()



    def create_vm(conn, vm_name, disk_size_gb, memory_size_mib, iso_choice, os_choice, network_choice):
        vm_name = vm_name
        disk_size_gb = disk_size_gb
        memory_size_mib = memory_size_mib
        iso_choice = iso_choice
        os_choice = os_choice
        network_choice = network_choice

        if vm_name == '' or disk_size_gb == '' or memory_size_mib == '' or iso_choice == '' or os_choice == '':
            messagebox.showwarning("Atenção!", "Preencha todos os campos!")
            return

        if not disk_size_gb.isdigit() or not memory_size_mib.isdigit():
            messagebox.showinfo("Atenção!", "Tamanho do disco e memória devem ser números inteiros!")
            return
        
        disk_size_gb = int(disk_size_gb)
        memory_size_mib = int(memory_size_mib)

        if disk_size_gb < 1:
            messagebox.showinfo("Atenção!", "O tamanho do disco deve ser maior que zero!")
            return
        
        if disk_size_gb > 1024:
            messagebox.showinfo("Atenção!", "O tamanho do disco deve ser menor que 1 TB!")
            return

        if memory_size_mib < 1024:
            messagebox.showinfo("Atenção!", "O tamanho da memória deve ser maior que 1 GB!")
            return

        host_memory = conn.getInfo()[1]
        if memory_size_mib > host_memory * 0.8:
            messagebox.showinfo("Atenção!", f"O limite da memória deve ser menor que 80% da memória total do host ({host_memory} MiB)!")
            return

        iso_choice_lower = iso_choice.lower()
        iso_path = f'/var/lib/libvirt/images/{iso_choice_lower}'
        if not os.path.exists(iso_path):
            if not os.path.exists(f'{iso_path}.iso'):
                messagebox.showinfo("Atenção!", f"Imagem ISO {iso_choice} não encontrada em /var/lib/libvirt/images/")
                return
            else:
                iso_path = f'{iso_path}.iso'

        os_choice_lower = os_choice.lower()
        if os_choice_lower not in ["linux", "windows", "solaris", "other", "generic"]:
            messagebox.showinfo("Atenção!", "Tipo de SO não suportado!\n Use 'generic' para outros.")
            return

        domains = conn.listAllDomains()
        domain_names = [domain.name() for domain in domains]
        if vm_name in domain_names:
            messagebox.showwarning("Atenção!", "O nome da VM já existe!")
            return
        
        if vm_name.isdigit():
            messagebox.showwarning("Atenção!", "O nome da VM não pode ser apenas números!")
            return
    
        try:
            disk_path = f'/var/lib/libvirt/images/{vm_name}.qcow2'
            os.system(f'sudo qemu-img create -f qcow2 {disk_path} {disk_size_gb}G')

            if os.path.exists('/sys/class/net/virbr0'):
                os.system(f'sudo virt-install --name {vm_name} --memory {memory_size_mib} --disk {disk_path} --cdrom {iso_path} --os-type {os_choice_lower} --network bridge:{network_choice} --graphics spice --noautoconsole')
                messagebox.showinfo("Sucesso!", f"VM {vm_name} criada com sucesso!")
            else:
                messagebox.showerror("Falha!", "A interface de rede virbr0 não foi encontrada no host!")
                return
        except libvirt.libvirtError as e:
            messagebox.showerror("Falha!", f'Erro ao criar VM {vm_name}: {e}')
            return
        

    def access_vm_with_spice(conn, vm_name):
        os.system('clear')
        try:
            domains = conn.listAllDomains()
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return

            domain = conn.lookupByName(vm_name)
            if not domain.isActive():
                print(f'Atenção: A VM "{vm_name}" está desligada!')
                return
            
            else:
                def open_remote_viewer(): 
                    xml_desc = domain.XMLDesc()
                    if '<graphics type' in xml_desc:
                        spice_port = xml_desc.split("<graphics type='")[1].split("port='")[1].split("' autoport")[0].strip()
                        spice_port = ''.join(filter(str.isdigit, spice_port))
                        os.system(f'remote-viewer spice://127.0.0.1:{spice_port}')
                    else:
                        print("Não foi possível obter a porta Spice da VM.")

                spice_thread = threading.Thread(target=open_remote_viewer)
                spice_thread.start()
        except libvirt.libvirtError as e:
            print(f'Erro ao obter informações da VM {vm_name}: {e}')


    def delete_vm(conn, vm_name):
        os.system('clear')
        try:
            domains = conn.listAllDomains()
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return
            
            domain = conn.lookupByName(vm_name)
            if domain.isActive():
                domain.destroy()
            domain.undefine()
            disk_path = f'/var/lib/libvirt/images/{vm_name}.qcow2'
            if os.path.exists(disk_path):
                os.remove(disk_path)
            print(f'VM {vm_name} excluída com sucesso.')
        except libvirt.libvirtError as e:
            print(f'Erro ao excluir VM {vm_name}: {e}')


    def allocate_resources_action(conn, vm_name):
        
        domains = conn.listAllDomains()
        domain_names = [domain.name() for domain in domains]

        if vm_name not in domain_names:
            messagebox.showwarning("Atenção", "A VM informada não existe!")
            return
                
        domain = conn.lookupByName(vm_name)
        if not domain.isActive():
        
            def back():
                labels_frame.destroy()
                root.destroy()

            conn = connect_to_libvirt()
            domain = conn.lookupByName(vm_name)


            def allocate_resources(conn, cpu_entry, memory_entry, disk_entry):
           
                cpu_entry = cpu_entry
                memory_entry = memory_entry
                disk_entry = disk_entry

                cpu = domain.info()[3]
                memory = domain.info()[2]
                disk_path = "/var/lib/libvirt/images/" + vm_name + ".qcow2"
                disk = domain.blockInfo(disk_path, 0)[0]
                disk_gb = disk / 1024 / 1024 / 1024

         
                if cpu_entry == '' and memory_entry == '' and disk_entry == '':
                    messagebox.showinfo("Valores Atuais Mantidos!", f"CPU: {cpu} \nMemória: {memory} KiB\nDisco: {disk_gb:.2f} GB")
                    back()
                    return

           
                if not cpu_entry.isdigit() or not memory_entry.isdigit() or not disk_entry.isdigit():
                    messagebox.showinfo("Atenção!", "Tamanho do disco, memória e CPU devem ser números inteiros!")
                    return
                
             
                cpu_entry = int(cpu_entry)
                memory_entry = int(memory_entry)
                disk_entry = int(disk_entry)

             
                if cpu_entry < 1:
                    messagebox.showinfo("Atenção!", "O número de CPUs deve ser maior que zero!")
                    return
                
                cpus_host = conn.getInfo()[2]
                if cpu_entry > cpus_host:
                    messagebox.showinfo("Atenção!", f"O número de CPUs deve ser menor que o número de CPUs do host ({cpus_host})!")
                    return
                
                if memory_entry < 1024:
                    messagebox.showinfo("Atenção!", "O tamanho da memória deve ser maior que 1 GB!")
                    return
                
                host_memory = conn.getInfo()[1]
                if memory_entry > host_memory * 0.8:
                    messagebox.showinfo("Atenção!", f"O limite da memória deve ser menor que 80% da memória total do host ({host_memory} MiB)!")
                    return
                
                if disk_entry < 1:
                    messagebox.showinfo("Atenção!", "O tamanho do disco deve ser maior que zero!")
                    return
                
                if disk_entry > 1024:
                    messagebox.showinfo("Atenção!", "O tamanho do disco deve ser menor que 1 TB!")
                    return
                    
                try:
                    xml_desc = conn.lookupByName(vm_name).XMLDesc()
                    new_xml_desc = xml_desc.replace(f"<vcpu placement='static'>{cpu}</vcpu>", f"<vcpu placement='static'>{cpu_entry}</vcpu>")
                    new_xml_desc = new_xml_desc.replace(f"<memory unit='KiB'>{memory}</memory>", f"<memory unit='KiB'>{memory_entry}</memory>")
                    conn.lookupByName(vm_name).undefine()
                    conn.defineXML(new_xml_desc)
                    if disk_entry != 0:
                        disk_path = "/var/lib/libvirt/images/" + vm_name + ".qcow2"
                        os.system(f'sudo qemu-img resize {disk_path} +{disk_entry}G')
                    messagebox.showinfo("Sucesso!", f"Recursos alocados\nCPU: {cpu_entry} vCPU(s)\nMemória: {memory_entry} KiB\nDisco: {disk_gb + disk_entry} GB")
                    back()
                    return
                except libvirt.libvirtError as e:
                    print(f'Erro ao alocar recursos para a VM {vm_name}: {e}')

             
                back()

            root = tk.Tk()
            root.title("Alocar Recursos")
            root.geometry("580x480")

       
            labels_frame = ttk.LabelFrame(root, text="Alocar Recursos")
            labels_frame.grid(row=0, column=0, padx=10, pady=10)

     
            cpu_label = ttk.Label(labels_frame, text="Alocar CPU:")
            cpu_label.grid(row=0, column=0, padx=10, pady=10)

            cpu_entry = ttk.Entry(labels_frame)
            cpu_entry.grid(row=0, column=1, padx=10, pady=10)

            memory_label = ttk.Label(labels_frame, text="Alocar memória (MiB):")
            memory_label.grid(row=1, column=0, padx=10, pady=10)

            memory_entry = ttk.Entry(labels_frame)
            memory_entry.grid(row=1, column=1, padx=10, pady=10)

        
            disk_label = ttk.Label(labels_frame, text="Alocar disco (GB):")
            disk_label.grid(row=2, column=0, padx=10, pady=10)

            disk_entry = ttk.Entry(labels_frame)
            disk_entry.grid(row=2, column=1, padx=10, pady=10)

           
            allocate_resources_button = ttk.Button(labels_frame, text="Alocar Recursos", command=lambda: allocate_resources(conn, cpu_entry.get(), memory_entry.get(), disk_entry.get()))
            allocate_resources_button.grid(row=3, column=0, padx=(0,5), pady=30)

            back_button = ttk.Button(labels_frame, text="Voltar", command=back)
            back_button.grid(row=3, column=1, padx=(5,0), pady=30)

            root.mainloop()

        else:
            print(f'Atenção: A VM "{vm_name}" está ligada! Desligue-a para alocar recursos.')
            return



    def get_vm_info(conn, vm_name):
        os.system('clear')
        try:
          
            domains = conn.listAllDomains()
            if not domains:
                print('Nenhuma VM encontrada.')
                return
            
         
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return
            
       
            domain = conn.lookupByName(vm_name)
            state, _ = domain.state()
            state_str = "Ligada" if state == libvirt.VIR_DOMAIN_RUNNING else "Desligada"

            print(f'Informações da VM {vm_name}:')
            print(f'Estado: {state_str}')

          
            xml_desc = domain.XMLDesc()
            print("Identificador Global para a VM:")
            if '<uuid>' in xml_desc:
                uuid = xml_desc.split("<uuid>")[1].split("</uuid>")[0].strip()
                print(f' - UUID: {uuid}')

            print("Configurações de CPU e Memória:")
            if '<vcpu' in xml_desc:
                cpu_info = xml_desc.split("<vcpu")[1].split("</vcpu>")[0].strip()
                num_vcpus = cpu_info.split("placement='static'>")[1].strip()
                print(f' - CPUs Virtuais: {num_vcpus}')

            if '<memory unit' in xml_desc:
                mem_info = xml_desc.split("<memory unit")[1].split("</memory>")[0].strip()
                mem_size = mem_info.split("='")[1].split("'>")[0]
                mem_unit = mem_info.split("'>")[1].strip()
                print(f' - Memória: {mem_unit} {mem_size}')

           
            print("Configurações de Disco:")
            if '<disk type' in xml_desc:
                disk_info = xml_desc.split("<disk type")[1].split("</disk>")[0].strip()
                disk_device = disk_info.split("device='")[1].split("'")[0].strip()
                disk_source = disk_info.split("<source file='")[1].split("'")[0].strip()
                disk_bus = disk_info.split("bus='")[1].split("'")[0].strip()
                disk_path = "/var/lib/libvirt/images/" + vm_name + ".qcow2"
                disk_in = domain.blockInfo(disk_path, 0)[0]
                disk_size_gb = disk_in / 1024 / 1024 / 1024
                print(f' - Dispositivo: {disk_device}')
                print(f' - Arquivo de Disco: {disk_source}')
                print(f' - Tamanho do armazenamento: {disk_size_gb:.2f} GB')
                print(f' - Barramento: {disk_bus}')

         
            if '<disk type' not in xml_desc:
                print("Configurações de CD-ROM:")
                print(" - Nenhuma imagem de CD-ROM inserida.")
            else:
             
                cdrom_info = xml_desc.split("<disk type")[2].split("</disk>")[0].strip()
                cdrom_device = cdrom_source = cdrom_bus = "N/A" 
                if "device='" in cdrom_info:
                    cdrom_device = cdrom_info.split("device='")[1].split("'")[0].strip()
                if "<source file='" in cdrom_info:
                    cdrom_source = cdrom_info.split("<source file='")[1].split("'")[0].strip()
                if "bus='" in cdrom_info:
                    cdrom_bus = cdrom_info.split("bus='")[1].split("'")[0].strip()
                cdrom_size = os.path.getsize(cdrom_source) if os.path.exists(cdrom_source) else 0
                cdrom_size_gb = int(cdrom_size) / 1024 / 1024 / 1024
                print("Configurações de CD-ROM:")
                print(f' - Dispositivo: {cdrom_device}')
                print(f' - Imagem ISO: {cdrom_source}')
                print(f' - Tamanho: {cdrom_size_gb:.2f} GB')
                print(f' - Barramento: {cdrom_bus}')
               
                   
            if '<interface type' in xml_desc:
                print("Configurações de Rede:")
                network_info = xml_desc.split("<interface type")[1].split("</interface>")[0].strip()
                network_model = network_info.split("model type='")[1].split("'/>")[0].strip()
                network_mac = network_info.split("mac address='")[1].split("'/>")[0].strip()
                network_source = network_info.split("<source bridge='")[1].split("'/>")[0].strip()
                print(f' - Modelo: {network_model}')
                print(f' - MAC: {network_mac}')
                print(f' - Fonte: {network_source}')

         
        except libvirt.libvirtError as e:
            print(f'Erro ao obter informações da VM {vm_name}: {e}')



    def snapshot_vm(conn, vm_name):
        os.system('clear')
        try:
            domains = conn.listAllDomains()
            if not domains:
                print('Nenhuma VM encontrada.')
                return
            
            domain_names = [domain.name() for domain in domains]
            if vm_name not in domain_names:
                messagebox.showwarning("Atenção", "A VM informada não existe!")
                return
        
            def back():
                labels_frame.destroy()
                root.destroy()
 
            def create_snapshot(conn, vm_name, snapshot_name):
                if snapshot_name == '':
                    messagebox.showwarning("Atenção!", "Preencha o nome do snapshot!")
                    return

                domain = conn.lookupByName(vm_name)
                snapshots = domain.snapshotListNames()
                if snapshot_name in snapshots:
                    messagebox.showwarning("Atenção!", "O nome do snapshot já existe!")
                    return

                try:
                    domain.snapshotCreateXML(f'<domainsnapshot><name>{snapshot_name}</name></domainsnapshot>', 0)
                    messagebox.showinfo("Sucesso!", f"Snapshot {snapshot_name} criado com sucesso!")
                except libvirt.libvirtError as e:
                    messagebox.showerror("Falha!", f'Erro ao criar snapshot {snapshot_name}: {e}')
                    return

            def list_snapshots(conn, vm_name):
                domains = conn.listAllDomains()
                domain_names = [domain.name() for domain in domains]
                if vm_name not in domain_names:
                    messagebox.showwarning("Atenção", "A VM informada não existe!")
                    return

                domain = conn.lookupByName(vm_name)
                snapshots = domain.snapshotListNames()
                if not snapshots:
                    messagebox.showinfo("Atenção!", "A VM não tem snapshots!")
                    return

                snapshots_str = ''
                for snapshot in snapshots:
                    snapshots_str += f'{snapshot}\n'
                messagebox.showinfo("Snapshots", "Snapshots atuais:\n" + snapshots_str)

            def delete_snapshot(conn, vm_name, snapshot_name):
                if snapshot_name == '':
                    messagebox.showwarning("Atenção!", "Preencha o nome do snapshot!")
                    return

                domain = conn.lookupByName(vm_name)
                snapshots = domain.snapshotListNames()
                if snapshot_name not in snapshots:
                    messagebox.showwarning("Atenção!", "O nome do snapshot não existe!")
                    return

                try:
                    domain.snapshotLookupByName(snapshot_name).delete()
                    messagebox.showinfo("Sucesso!", f"Snapshot {snapshot_name} excluído com sucesso!")
                except libvirt.libvirtError as e:
                    messagebox.showerror("Falha!", f'Erro ao excluir snapshot {snapshot_name}: {e}')
                    return

          

            root = tk.Tk()
            root.title("Snapshot")
            root.geometry("435x120")

            labels_frame = ttk.LabelFrame(root, text="Escolha uma opção abaixo")
            labels_frame.grid(row=0, column=0, padx=5, pady=5)

            snapshot_name_label = ttk.Label(labels_frame, text="Nome do snapshot:")
            snapshot_name_label.grid(row=0, column=0, padx=10, pady=10)

            snapshot_name_entry = ttk.Entry(labels_frame)
            snapshot_name_entry.grid(row=0, column=1, padx=5, pady=10)

            create_snapshot_button = ttk.Button(labels_frame, text="Criar", command=lambda: create_snapshot(conn, vm_name, snapshot_name_entry.get()))
            create_snapshot_button.grid(row=1, column=0, pady=5, padx=(15, 0), sticky='w')

            list_snapshots_button = ttk.Button(labels_frame, text="Listar", command=lambda: list_snapshots(conn, vm_name))
            list_snapshots_button.grid(row=1, column=1, pady=10, padx=(0,35))

            delete_snapshot_button = ttk.Button(labels_frame, text="Excluir", command=lambda: delete_snapshot(conn, vm_name, snapshot_name_entry.get()))
            delete_snapshot_button.grid(row=1, column=2, pady=10, padx=(0, 15), sticky='e')

            root.mainloop()
                        
           
        except libvirt.libvirtError as e:
            print(f'Erro ao obter informações da VM {vm_name}: {e}')


    def changelog():
  
        wn = turtle.Screen()
        wn.title("Sobre o Sys-ControlVMs")
        wn.bgpic("about.png")
        wn.setup(width=600, height=600)
        wn.tracer(0)


    conn = connect_to_libvirt()

    root = tk.Tk()
    root.title("Sys-ControlVMs")
    root.geometry("730x520")

    labels_frame = ttk.LabelFrame(root, text="Bem-vindo ao Sys-ControlVMs!")
    labels_frame.grid(row=0, column=0, padx=10, pady=10)

    vm_name_label = ttk.Label(labels_frame, text="Nome da VM:")
    vm_name_label.grid(row=0, column=0, padx=10, pady=10)

    vm_name_entry = ttk.Entry(labels_frame)
    vm_name_entry.grid(row=0, column=1, padx=10, pady=10)

    list_vms_button = ttk.Button(labels_frame, text="Listar", command=lambda: list_vms(conn))
    list_vms_button.grid(row=1, column=0, columnspan=2, padx=(0,110), pady=10)

    start_vm_button = ttk.Button(labels_frame, text="Ligar", command=lambda: start_vm(conn, vm_name_entry.get()))
    start_vm_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    stop_vm_button = ttk.Button(labels_frame, text="Desligar", command=lambda: stop_vm(conn, vm_name_entry.get()))
    stop_vm_button.grid(row=2, column=0, columnspan=2, padx=(0,110), pady=10)

    
    create_vm_button = ttk.Button(labels_frame, text="Criar", command=create_vm_action)
    create_vm_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

   
    delete_vm_button = ttk.Button(labels_frame, text="Excluir", command=lambda: delete_vm(conn, vm_name_entry.get()))
    delete_vm_button.grid(row=3, column=0, columnspan=2, padx=(0,110), pady=10)

    get_vm_info_button = ttk.Button(labels_frame, text="Informações", command=lambda: get_vm_info(conn, vm_name_entry.get()))
    get_vm_info_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)


    allocate_resources_button = ttk.Button(labels_frame, text="Alocar Recursos", command=lambda: allocate_resources_action(conn, vm_name_entry.get()))
    allocate_resources_button.grid(row=4, column=0, columnspan=2, padx=(0,110), pady=10)

   
    access_vm_with_spice_button = ttk.Button(labels_frame, text="Acessar", command=lambda: access_vm_with_spice(conn, vm_name_entry.get()))
    access_vm_with_spice_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

    snapshot_vm_button = ttk.Button(labels_frame, text="Snapshot", command=lambda: snapshot_vm(conn, vm_name_entry.get()))
    snapshot_vm_button.grid(row=5, column=0, columnspan=2, padx=(0,110), pady=10)

    changelog_button = ttk.Button(labels_frame, text="Sobre o SCVMs", command=changelog)
    changelog_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)


    labels_frame = ttk.LabelFrame(root, text="Log")
    labels_frame.grid(row=0, column=1, padx=5, pady=5)

    text_widget = tk.Text(labels_frame, width=45)
    text_widget.grid(row=0, column=1, padx=5, pady=5)

    class StdoutRedirector(object):
        def __init__(self, text_widget):
            self.text_space = text_widget
            self.buffer = ""

        def write(self, string):
            self.buffer += string
            self.text_space.insert(tk.END, self.buffer)
            self.buffer = ""
            self.text_space.see(tk.END)          

        

        def flush(self):
            pass
    sys.stdout = StdoutRedirector(text_widget)

    def clear_text():
        text_widget.delete('1.0', tk.END)

    clear_log_button = ttk.Button(labels_frame, text="Limpar Log", command=clear_text)
    clear_log_button.grid(row=1, column=1, padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    gui()
