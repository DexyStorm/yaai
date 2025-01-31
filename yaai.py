import subprocess 
import os
import sys
import pexpect




def get_y_n(question: str) -> str:
   
	user_input: str = 'ligma'

	while( not(user_input == "y" or user_input == "n")):
		user_input = input(question + "\n")
		

	
	return user_input







def get_input(question: str) -> str:

	user_input = input(question + "\n")

	return user_input




def ask_if_proceed_with_install(question: str):

	input: str = get_y_n(question)

	if(input == "y"):
		return

	print("exiting...")
	sys.exit()


def ask_if_encryption(question: str) -> bool:

	input: str = get_y_n(question)

	if(input == "y"):
		return True
	
	return False

def format_partitions(encryption: bool, root: str, boot: str, swap: str):
	if(encryption == True):
		subprocess.run(["clear"], shell=True)
		subprocess.run(["sudo pacman -Sy cryptsetup lvm2 --noconfirm && sudo cryptsetup luksFormat /dev/" + root], shell=True)

		subprocess.run(["cryptsetup open /dev/" + root + " " + root], shell=True)
		

		subprocess.run(["sudo mkfs.ext4 /dev/mapper/" + root], shell=True)
		subprocess.run(["sudo mount /dev/mapper/" + root + " /mnt"], shell=True)
	else:
		subprocess.run(["sudo mkfs.ext4 /dev/" + root], shell=True)
		subprocess.run(["sudo mount /dev/" + root + " /mnt"], shell=True)

	subprocess.run(["mkfs.fat -F32 /dev/" + boot], shell=True)
	subprocess.run(["sudo mkswap /dev/" + swap + "&& sudo swapon /dev/" + swap], shell=True)
	
	subprocess.run(["sudo mkdir /mnt/boot"], shell=True)
	subprocess.run(["sudo mount /dev/" + boot + " /mnt/boot"], shell=True)


def fix_grub():


def fix_files(username, encryption):
	fix_grub()
	fix_sudoers()
	if(encryption == "y"):
		fix_mkinitcpio()
		fix_fstab()



def install_system():
	novideo: str = get_input("Do you use a Nvidia GPU? (y/n)")
	subprocess.run(["sudo pacstrap -K /mnt linux-zen discord sudo git wget curl vlc linux-zen-headers firefox networkmanager base base-devel vim nano cryptsetup lvm2 grub efibootmgr"], shell=True)
	
	subprocess.run(["genfstab -U /mnt >> /mnt/etc/fstab"], shell=True)

	subprocess.run(["arch-chroot /mnt"], shell=True)

	if(novideo == "y"):
		subprocess.run(["nvidia-dkms nvidia-utils nvidia-settings"], shell=True)

	subprocess.run(["hwclock --systohc"], shell=True)
	subprocess.run(["locale-gen"], shell=True)
	subprocess.run(["LANG=en_US.UTF-8"], shell=True)
	subprocess.run(["grub-install --target=x86_64-efi --efi-directory=/boot --root-directory=/ --bootloader-id=GRUB"], shell=True)
	subprocess.run(["mkinitcpio -p linux-zen && sudo grub-mkconfig -o /boot/grub/grub.cfg"], shell=True)
	subprocess.run(["systemctl enable NetworkManager"], shell=True)

	hostname: str = get_input("Enter your Hostname aka PC's name")
	subprocess.run([f"echo {hostname} > /etc/hostname"], shell=True)

	username: str = get_input("Enter your Username")
	subprocess.run(["useradd -mg wheel dexystorm"], shell=True)

	print("Enter the password for " + username)
	subprocess.run(["passwd " + username], shell=True)

	print("Enter your Root password")
	subprocess.run(["passwd"], shell=True)



	fix_files(username, encryption)
	 
	subprocess.run(["mkinitcpio -p linux-zen && sudo grub-mkconfig -o /boot/grub/grub.cfg"], shell=True)




def partitions(root: str, boot: str, swap: str):

	confirmation_for_partitions = "n"
	while(confirmation_for_partitions == "n"):
		subprocess.run(["lsblk"], shell=True)
		root = get_input("Please enter your root partition")
		boot = get_input("Please enter your boot partition")
		swap = get_input("Please enter your swap partition. If you don't have a swap partition, just hit enter")
		
		question: str = "Here are your partition names. Are they correct? (y/n)\n"
		question = question + "root: " + root + "\nboot: " + boot + "\nswap: "

		if(len(swap) == 0):
			question = question + "No Swap"
		else:
			question = question + swap

		confirmation_for_partitions = get_y_n(question)



	encryption: bool = ask_if_encryption("Do you want to encrypt your boot drive? (y/n)")

	format_partitions(encryption, root, boot, swap)
	
	install_system(encryption)








if __name__ == "__main__":

	print("This will install a Arch Linux Distro on your PC with DexyStorm's preferred settings.")
	print("This isntall is supposed to be used on a FRESH Arch ISO")
	print("")

	print("Here are some settings that Dexy likes to use for his Arch distro and some requirements:")
	print("This Installation assumes that you have an Internect connection and that you have a UEFI motherboard and are booted with UEFI.")
	print("For this installation you need to already have set up your disk partitions. If you have not done that yet, go do it and come back afterwards.")
	print("The Kernel which will be installed is linux-zen.")



	ask_if_proceed_with_install("Do you want to continue?");
	
	root: str = ""
	boot: str = ""
	swap: str = ""
	partitions(root, boot, swap)