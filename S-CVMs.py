import libvirt
import sys
import os
import re

#   Sys-ControlVMs - VMs management with libvirt
#   
#   S-CVMs.py - Script para o funcionamento do Sys-ControlVMs
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
#   $ sudo python3 S-CVMs.py
#
# -----------------------------------------------------------------------------
#
#   ChangeLog:
#
#   v1.0 18/09/2023, Thiago Abrante
#     - Primeira versão!
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
    os.system('clear')
    print()
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
    except libvirt.libvirtError as e:
        print(f'Erro ao listar VMs: {e}')
    

def start_vm(conn, vm_name):
    os.system('clear')
    print()
    try:
      
        domains = conn.listAllDomains()
        domain_names = [domain.name() for domain in domains]
        if vm_name not in domain_names:
            print(f'A VM {vm_name} não existe.')
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
    print()
    try:
       
        domains = conn.listAllDomains()
        domain_names = [domain.name() for domain in domains]
        if vm_name not in domain_names:
            print(f'A VM {vm_name} não existe.')
            return
        domain = conn.lookupByName(vm_name)
        if not domain.isActive():
            print(f'A VM {vm_name} já está desligada.')
        else:
          
            domain.destroy()
            print(f'A VM {vm_name} foi desligada.')
    except libvirt.libvirtError as e:
        print(f'Erro ao desligar VM {vm_name}: {e}')

def create_vm(conn):
    os.system('clear')
    print()
    try:
        
        vm_name = input('Digite o nome da nova VM: ').strip()
        while not vm_name or vm_name.isdigit():
            print("O nome da VM não pode ser vazio ou apenas números.")
            vm_name = input('Digite o nome da nova VM: ').strip()

    
        disk_size_gb = input('Tamanho do disco (por exemplo, 10G): ').strip()
        while not disk_size_gb.isdigit():
            print("O tamanho do disco deve ser um número válido.")
            disk_size_gb = input('Tamanho do disco (por exemplo, 10G): ').strip()

   
        memory_size_mib = input('Tamanho da memória (por exemplo, 2048 MiB): ').strip()
        while not memory_size_mib.isdigit():
            print("O tamanho da memória deve ser um número válido.")
            memory_size_mib = input('Tamanho da memória (por exemplo, 2048 MiB): ').strip()

       
        iso_directory = '/var/lib/libvirt/images'

   
        iso_options = [f for f in os.listdir(iso_directory) if f.endswith('.iso')]
        if not iso_options:
            print(f"Nenhuma imagem ISO encontrada em {iso_directory}")
            dub_iso = input("Deseja copiar uma imagem ISO para esse diretório? (S/N) ").strip().lower()
            while dub_iso not in ['s', 'n']:
                print("Escolha inválida. Digite S para sim ou N para não.")
                dub_iso = input("Deseja copiar uma imagem ISO para esse diretório? (S/N) ").strip().lower()
            
            if dub_iso == 's':
                while True:
                    location_iso = input("Digite o caminho completo da imagem ISO: ").strip()
                    if not os.path.exists(location_iso):
                        print("O caminho especificado não existe.")
                    else:
                        iso_files = [f for f in os.listdir(location_iso) if f.endswith('.iso')]
                        if not iso_files:
                            print("O caminho especificado não contém nenhuma imagem ISO. Tente novamente.")
                        else:
                            print(f"Copiando imagens ISO de {location_iso} para {iso_directory}...")
                            for iso_file in iso_files:
                                os.system(f'sudo cp "{os.path.join(location_iso, iso_file)}" {iso_directory}')
                            iso_options = [f for f in os.listdir(iso_directory) if f.endswith('.iso')]
                            print("Imagens ISO disponíveis:")
                            for i, iso_file in enumerate(iso_options, start=1):
                                print(f"{i}. {iso_file}")
                            break
            else:
                print("Não é possível criar uma VM sem uma imagem ISO.")
                return
        else:
           
            print("Imagens ISO disponíveis:")
            for i, iso_file in enumerate(iso_options, start=1):
                print(f"{i}. {iso_file}")

     
        iso_choice = input("Escolha o número da imagem ISO desejada: ").strip()
        while not iso_choice.isdigit() or int(iso_choice) < 1 or int(iso_choice) > len(iso_options):
            print("Escolha inválida. Digite o número correspondente à imagem ISO desejada.")
            iso_choice = input("Escolha o número da imagem ISO desejada: ").strip()

        selected_iso = iso_options[int(iso_choice) - 1]
        iso_path = os.path.join(iso_directory, selected_iso)

       
        os_types = ["linux", "windows", "bsd", "macos", "other"]
        print("Tipos de sistema operacional disponíveis:")
        for i, os_type in enumerate(os_types):
            print(f"{i + 1}. {os_type}")
        os_choice = input("Escolha o número do tipo de sistema operacional: ").strip()
        while not os_choice.isdigit() or int(os_choice) < 1 or int(os_choice) > len(os_types):
            print("Escolha inválida. Digite o número correspondente ao tipo de sistema operacional desejado.")
            os_choice = input("Escolha o número do tipo de sistema operacional: ").strip()
        selected_os_type = os_types[int(os_choice) - 1]

    
        network_names = ["virbr0"]
        print("Interface de rede disponível:")
        for i, network_name in enumerate(network_names):
            print(f"{i + 1}. {network_name}")
        network_choice = input("Escolha o número do nome de rede: ").strip()
        while not network_choice.isdigit() or int(network_choice) < 1 or int(network_choice) > len(network_names):
            print("Escolha inválida. Digite o número correspondente ao nome de rede desejado.")
            network_choice = input("Escolha o número do nome de rede: ").strip()
        selected_network_name = network_names[int(network_choice) - 1]

        
        qcow2_path = f'/var/lib/libvirt/images/{vm_name}.qcow2'
        if not os.path.exists(qcow2_path):
            print(f'A imagem de disco {qcow2_path} não existe. Criando...')
            os.system(f'sudo qemu-img create -f qcow2 {qcow2_path} {disk_size_gb}')
        else:
            print(f'A imagem de disco {qcow2_path} já existe em {qcow2_path}.')

        vm_exists = os.system(f'sudo virsh list --all | grep {vm_name}')
        if vm_exists == 0:
            print(f'A VM {vm_name} já existe!')
        else:
            os.system(f'sudo virt-install --name {vm_name} --memory {memory_size_mib} --disk {qcow2_path} --cdrom {iso_path} --os-type {os_type} --network bridge:{network_name} --graphics vnc --noautoconsole')
            print(f'VM {vm_name} criada com sucesso.')
    except libvirt.libvirtError as e:
        print(f'Erro ao criar VM {vm_name}: {e}')

def delete_vm(conn, vm_name):
    os.system('clear')
    print()
    try:
      
        domains = conn.listAllDomains()
        domain_names = [domain.name() for domain in domains]
        if vm_name not in domain_names:
            print(f'A VM {vm_name} não existe.')
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

def get_vm_info(conn, vm_name):
    os.system('clear')
    print()
    try:
      
        domains = conn.listAllDomains()
        if not domains:
            print('Nenhuma VM encontrada.')
            return
        
    
        domain_names = [domain.name() for domain in domains]
        if vm_name not in domain_names:
            print(f'A VM {vm_name} não existe.')
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
            disk_size = os.path.getsize(disk_source)
            disk_size_gb = int(disk_size) / 1024 / 1024 / 1024
            print(f' - Dispositivo: {disk_device}')
            print(f' - Arquivo de Disco: {disk_source}')
            print(f' - Tamanho do armazenamento: {disk_size_gb:.2f} GB')
            print(f' - Barramento: {disk_bus}')

   
        print("Configurações de CD-ROM:")
        if '<disk type' in xml_desc:
            cdrom_info = xml_desc.split("<disk type")[2].split("</disk>")[0].strip()
            cdrom_device = cdrom_info.split("device='")[1].split("'")[0].strip()
            cdrom_source = cdrom_info.split("<source file='")[1].split("'")[0].strip()
            cdrom_bus = cdrom_info.split("bus='")[1].split("'")[0].strip()
            cdrom_size = os.path.getsize(cdrom_source)
            cdrom_size_gb = int(cdrom_size) / 1024 / 1024 / 1024
            print(f' - Dispositivo: {cdrom_device}')
            print(f' - Arquivo de Disco: {cdrom_source}')
            print(f' - Tamanho do disco: {cdrom_size_gb:.2f} GB')
            print(f' - Barramento: {cdrom_bus}')
        else:
            print("Nenhuma imagem ISO encontrada.")

     
        if '<interface type' in xml_desc:
            print("Configurações de Rede:")
            network_info = xml_desc.split("<interface type")[1].split("</interface>")[0].strip()
            network_model = network_info.split("model type='")[1].split("'/>")[0].strip()
            network_mac = network_info.split("mac address='")[1].split("'/>")[0].strip()
            network_source = network_info.split("<source bridge='")[1].split("'/>")[0].strip()
            print(f' - Modelo: {network_model}')
            print(f' - MAC: {network_mac}')
            print(f' - Fonte: {network_source}')

        
        def allocate_resources():
            if not domain.isActive():
                print()
                while True:
                    print("Deseja alocar recursos para a VM?")
                    print("1. Sim")
                    print("2. Não")
                    choice = input("Escolha uma opção: ")

                    if choice == '1':
                        print()
                        print("Alocação de recursos: Quais configurações você deseja alterar?")
                        while True:
                            print("1. CPU")
                            print("2. Memória")
                            print("3. Tamanho do Disco")
                            print("4. Voltar")
                            resource_choice = input("Escolha uma opção: ")

                            if resource_choice == '1':
                           
                                num_vcpus = int(input("Digite o número de CPUs virtuais desejadas: "))
                                xml_desc = conn.lookupByName(vm_name).XMLDesc()
                                current_vcpus = int(re.search(r"<vcpu placement='static'>(\d+)</vcpu>", xml_desc).group(1))
                                if num_vcpus < 1:
                                    print("O número de CPUs virtuais deve ser maior que zero.")
                                elif num_vcpus > 8:
                                    print("O número de CPUs virtuais não pode ser maior que 8.")
                                elif num_vcpus == current_vcpus:
                                    print("Número de CPUs virtuais não alterado pois o valor atual é o mesmo que o valor solicitado.")
                                else:
                                    new_xml_desc = xml_desc.replace(f"<vcpu placement='static'>{current_vcpus}</vcpu>", f"<vcpu placement='static'>{num_vcpus}</vcpu>")
                                    try:
                                        conn.defineXML(new_xml_desc)
                                        if num_vcpus > 6:
                                            print("Atenção! O Sobrecarregamento de CPUs virtuais pode causar problemas de desempenho. Valor alterado!")
                                        else:
                                            print(f"Número de CPUs virtuais definido como {num_vcpus}.")
                                    except libvirt.libvirtError as e:
                                        print(f"Erro ao definir o número de CPUs virtuais: {e}")

                            elif resource_choice == '2':
                            
                                mem_size_mib_str = input("Digite o tamanho da memória em MiB: ")
                               
                                mem_size_kib = int(mem_size_mib_str) * 1024
                                xml_desc = conn.lookupByName(vm_name).XMLDesc()
                                current_mem_size_kib = int(re.search(r"<memory unit='KiB'>(\d+)</memory>", xml_desc).group(1))
                                if mem_size_kib < 1024:
                                    print("O tamanho da memória deve ser maior que 1024 KiB.")
                                elif mem_size_kib > 15625000:
                                    print("O tamanho da memória não pode ser maior que 16 GB.")
                                elif mem_size_kib == current_mem_size_kib:
                                    print("Tamanho da memória não alterado pois o valor atual é o mesmo que o valor solicitado.")
                                else:
                                    new_xml_desc = xml_desc.replace(f"<memory unit='KiB'>{current_mem_size_kib}</memory>", f"<memory unit='KiB'>{mem_size_kib}</memory>")
                                    try:
                                        conn.defineXML(new_xml_desc)
                                        print(f"Tamanho da memória definido como {mem_size_kib / 1024} MiB.")
                                    except libvirt.libvirtError as e:
                                        print(f"Erro ao definir o tamanho da memória: {e}")
                            elif resource_choice == '3':
                                
                                disk_size_gb = int(input("Digite o tamanho do disco em GB: "))
                                disk_path = f'/var/lib/libvirt/images/{vm_name}.qcow2'
                                if disk_size_gb < 1:
                                    print("O tamanho do disco deve ser maior que zero.")
                                elif disk_size_gb > 1024:
                                    print("O tamanho do disco não pode ser maior que 1 TB.")
                                elif disk_size_gb == os.path.getsize(disk_path) / 1024 / 1024 / 1024:
                                    print("Tamanho do disco não alterado pois o valor atual é o mesmo que o valor solicitado.")
                                else:
                                    try:
                                        os.system(f'sudo qemu-img resize {disk_path} {disk_size_gb}G')
                                        print(f"Tamanho do disco definido como {disk_size_gb} GB.")
                                    except libvirt.libvirtError as e:
                                        print(f"Erro ao definir o tamanho do disco: {e}")
                                
                            elif resource_choice == '4':
                                break
                            
                            else:
                                print()
                                print("Opção inválida. Tente novamente.")

                    elif choice == '2':
                        break
                    else:
                        print()
                        print("Opção inválida. Tente novamente.")
            else:
                print("VM Ligada! Não é possível alterar as configurações de recursos.")

        allocate_resources()
    except libvirt.libvirtError as e:
        print(f'Erro ao obter informações da VM {vm_name}: {e}')

def snapshot_vm(conn, vm_name):
    os.system('clear')
    print()
    try:
     
        domains = conn.listAllDomains()
        if not domains:
            print('Nenhuma VM encontrada.')
            return
        
        
        domain_names = [domain.name() for domain in domains]
        if vm_name not in domain_names:
            print(f'A VM {vm_name} não existe.')
            return
        
        
        domain = conn.lookupByName(vm_name)
        state, _ = domain.state()
        state_str = "Ligada" if state == libvirt.VIR_DOMAIN_RUNNING else "Desligada"

        print(f'Informações da VM {vm_name}:')
        print(f'Estado: {state_str}')

       
        def snapshot_menu():
            while True:
                print()
                print("Opções:")
                print("1. Criar snapshot")
                print("2. Listar snapshots")
                print("3. Excluir snapshot")
                print("4. Voltar")
                choice = input("Escolha uma opção: ")

                if choice == '1':
                    print()
                    snapshot_name = input("Digite o nome do snapshot: ")
                    check1 = os.system(f'sudo virsh snapshot-list --domain {vm_name} | grep {snapshot_name}')
                    if check1 == 0:
                        print(f"Já existe um snapshot com o nome {snapshot_name}.")
                    else:
                        os.system(f'sudo virsh snapshot-create-as --domain {vm_name} --name {snapshot_name}')
                        print(f"Snapshot {snapshot_name} criado com sucesso.")
                elif choice == '2':
                    os.system(f'sudo virsh snapshot-list --domain {vm_name}')
                elif choice == '3':
                    snapshot_name = input("Digite o nome do snapshot: ")
                    check2 = os.system(f'sudo virsh snapshot-list --domain {vm_name} | grep {snapshot_name}')
                    if check2 == 0:
                        os.system(f'sudo virsh snapshot-delete --domain {vm_name} --snapshotname {snapshot_name}')
                        print(f"Snapshot {snapshot_name} excluído com sucesso.")
                    else:
                        print(f"Snapshot {snapshot_name} não encontrado.")
                elif choice == '4':
                    return
                else:
                    print("Opção inválida. Tente novamente.")
                    snapshot_menu()
                    
        snapshot_menu()
    except libvirt.libvirtError as e:
        print(f'Erro ao obter informações da VM {vm_name}: {e}')

def changelog():
    os.system('clear')
    print()
    print('Changelog:')
    print()
    print("Versão 1.0.0"), 
    print("v1.0 18/09/2023, Thiago Abrante")


def main():
    conn = connect_to_libvirt()

    while True:
        print("\nOpções:")
        print("1. Listar VMs")
        print("2. Iniciar VM")
        print("3. Parar VM")
        print("4. Criar VM")
        print("5. Excluir VM")
        print("6. Informações da VM/Alocação de recursos")
        print("7. Snapshot")
        print("8. Changelog")
        print("9. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            list_vms(conn)
        elif choice == '2':
            print()
            if not conn.listAllDomains():
                print('Nenhuma VM encontrada.')
                continue
            list_vms(conn)
            vm_name = input("Digite o nome da VM que deseja iniciar: ")
            start_vm(conn, vm_name)
        elif choice == '3':
            print()
            if not conn.listAllDomains():
                print('Nenhuma VM encontrada.')
                continue
            list_vms(conn)
            vm_name = input("Digite o nome da VM que deseja parar: ")
            stop_vm(conn, vm_name)
        elif choice == '4':
            create_vm(conn)
        elif choice == '5':
            print()
            if not conn.listAllDomains():
                print('Nenhuma VM encontrada.')
                continue
            list_vms(conn)
            vm_name = input("Digite o nome da VM que deseja excluir: ")
            delete_vm(conn, vm_name)
        elif choice == '6':
            print()
            if not conn.listAllDomains():
                print('Nenhuma VM encontrada.')
                continue
            list_vms(conn)
            vm_name = input("Digite o nome da VM que deseja obter informações: ")
            get_vm_info(conn, vm_name)
        elif choice == '7':
            print()
            if not conn.listAllDomains():
                print('Nenhuma VM encontrada.')
                continue
            list_vms(conn)
            vm_name = input("Digite o nome da VM: ")
            snapshot_vm(conn, vm_name)
        elif choice == '8':
            changelog()
        elif choice == '9':
            conn.close()
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()