# bookworm.md
```
noir: laptop
rose: raspberry pi (4)
```

# contents
- [noir config](#noir-config)
  - [install](#install)
  - [packages](#packages)
    - [sources](#sources)
    - [list of packages](#list-of-packages)
    - [general considerations](#general-considerations)
    - [condensed package install](#condensed-package-install)
      - [apt](#apt)
      - [nix](#nix)
      - [source](#source)
  - [additional config](#additional-config)
    - [locale](#locale)
    - [timedatectl](#timedatectl)
    - [grub](#grub)
    - [ufw](#ufw)
    - [AppArmor](#apparmor)
    - [NetworkManager](#networkmanager)
    - [bluetooth](#bluetooth)
    - [auto-cpufreq](#auto-cpufreq)
    - [powertop](#powertop)
    - [cups](#cups)
    - [keyring](#keyring)
    - [root account](#root-account)
    - [rust](#rust)
    - [timeshift](#timeshift)

- [rose config](#rose-config)
  - [install](#install-1)
  - [packages](#packages-1)
    - [sources](#sources-1)
    - [list of packages](#list-of-packages-1)
  - [additional config](#additional-config-1)
    - [sudo](#sudo)
    - [ssh](#ssh)
    - [ufw](#ufw-1)
    - [NetworkManager](#networkmanager-1)
    - [cryptsetup](#cryptsetup)
    - [syncthing](#syncthing)

- [security](#security)
  - [noir](#noir)
    - [attack surfaces](#attack-surfaces)
    - [physical access](#physical-access)
    - [packages](#packages-2)
      - [apt & repositories](#apt--repositories)
      - [nix](#nix-1)
      - [from source](#from-source)
      - [future considerations](#future-considerations)
    - [user accounts](#user-accounts)
    - [network](#network)
    - [browser](#browser)
    - [passwords](#passwords)
  - [rose](#rose)
    - [attack surfaces](#attack-surfaces-1)
    - [physical access](#physical-access-1)
    - [packages](#packages-3)
    - [user accounts](#user-accounts-1)
    - [network](#network-1)
  - [backups (only for noir)](#backups-only-for-noir)
    - [git setup for home directory](#git-setup-for-home-directory)

- [vms](#vms)
  - [setup](#setup)

# noir config

## install

1. debian 12 (bookworm)
2. use netisnt iso
3. skip root password
4. use LUKS encryption
5. select nothing in `tasksel`

## packages

### sources

all packages are from **apt**

some packages are from **nix**

to install nix

`$ sh <(curl -L https://nixos.org/nix/install) --daemon`

currently installed nix packages
```
swayfx
brave
rustup
vscodium
fastfetch
ags
cliphist
nixGLIntel
```
a short reason for using each of these packages can be found in the security section

only one package is installed from **source**
```
auto-cpufreq
```

### general considerations
1. prefer open source apps over proprietary ones
2. do not add new non-debian repositories to apt
3. non-free apt & nix pacakges not allowed, use web interface (eg. spotify)
4. prefer gtk over qt for *new* apps

### list of packages

1. sway & related
    ```
    sway
    swayfx [NIX]
    swayidle
    swaylock
    waybar
    wofi
    dunst
    foot
    brightnessctl
    slurp
    grimshot
    cliphist [NIX]
    python3-i3ipc
    ags [NIX]
    ```

2. terminal goodies
    ```
    fastfetch [NIX]
    cava
    fortune
    rig
    ```

3. development
    ```
    git
    python3
    rustup [NIX]
    virtualenvwrapper
    vscodium [NIX]
    ```

4. network
    ```
    network-manager
    ufw
    cups
    openssh-client
    systemd-timesyncd
    brave [NIX]
    wget
    curl
    ```

5. media
    ```
    playerctl
    gir1.2-playerctl-2.0
    pulseaudio
    pavucontrol
    wireplumber
    pipewire-media-session-
    gstreamer1.0-pipewire
    easyeffects
    swayimg
    mpv
    ```

7. filesystem
    ```
    nemo
    gparted
    xfsprogs
    ntfs-3g
    sshfs
    smartmontools
    timeshift
    ```

8. keys
    ```
    mate-polkit
    keepassxc
    gnome-keyring
    seahorse
    git-crypt
    ```

9. utilities
    ```
    apparmor-utils
    htop
    bpytop
    auto-cpufreq [SRC]
    blueman
    powertop
    qt5ct
    nixGLIntel [NIX]
    ```

10. editing
    ```
    micro
    mousepad
    inkscape
    libreoffice
    libreoffice-gtk3
    ```

11. fonts (other theme related fonts are in ~/.local/share/fonts)
    ```
    fonts-noto
    ```

12. games
    ```
    supertuxkart
    ```

### condensed package install

#### apt

1. install packages

    `# apt install sway swayidle swaylock waybar wofi dunst foot brightnessctl slurp grimshot python3-i3ipc cava fortune rig git python3 virtualenvwrapper network-manager ufw cups openssh-client systemd-timesyncd wget curl playerctl gir1.2-playerctl-2.0 pulseaudio pavucontrol wireplumber pipewire-media-session- gstreamer1.0-pipewire easyeffects swayimg mpv nemo gparted xfsprogs ntfs-3g sshfs smartmontools timeshift mate-polkit keepassxc gnome-keyring seahorse git-crypt apparmor-utils htop bpytop blueman powertop qt5ct micro mousepad inkscape libreoffice libreoffice-gtk3 fonts-noto supertuxkart -y`

#### nix

1. install nix

    `$ sh <(curl -L https://nixos.org/nix/install) --daemon`

2. install nix packages

    `$ nix-env -iA nixpkgs.swayfx nixpkgs.brave nixpkgs.rustup nixpkgs.vscodium nixpkgs.fastfetch nixpkgs.ags nixpkgs.cliphist`

3. and install nixGLIntel for launching GL nix applications

    `$ nix-channel --add https://github.com/nix-community/nixGL/archive/main.tar.gz nixgl && nix-channel --update`

    `$ nix-env -iA nixgl.nixGLIntel`

#### source

`$ git clone https://github.com/AdnanHodzic/auto-cpufreq`

`$ cd auto-cpufreq`

`# ./auto-cpufreq-installer`

## additional config

### locale

1. write line LANG=C.UTF-8 to /etc/default/locale, or

    `# echo "LANG=C.UTF-8" > /etc/default/locale`

2. write line en_US.UTF-8 UTF-8 to /etc/locale.gen, or

    `# echo "en_US.UTF-8 UTF-8" > /etc/locale.gen`

3. then regenerate locales

    `# locale-gen`


### timedatectl

1. enable ntp (network time protocol)

    `# timedatectl set-ntp true`

2. disable local rtc

    `# timedatectl set-local-rtc false`

### grub

1. edit the file /etc/default/grub to add these options to GRUB_CMDLINE_LINUX_DEFAULT

    1. quiet (for quiet booting)
    2. loglevel=1 (to prevent printing acpi errors during boot)
    3. rtc_cmos.use_acpi_alarm=1 (for bettery battery life) 

    `# sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet loglevel=1 rtc_cmos.use_acpi_alarm=1"/' /etc/default/grub`

2. uncomment and change GRB_GFXMODE to 1920x1200 or similar

    `# sed -i '/^#GRUB_GFXMODE/s/^#//; s/^GRUB_GFXMODE=.*/GRUB_GFXMODE=<var>resolution</var>/' /etc/default/grub`

3. write RESUME=none to /etc/initramfs-tools/conf.d/resume

    `# echo 'RESUME=none' | tee /etc/initramfs-tools/conf.d/resume`

3. update grub and initramfs

    `# update-grub`

    `# update-initramfs -u`

### ufw

1. enable ufw

    `# ufw enable`

2. check status

    `# ufw status verbose`

### AppArmor

1. check status to ensure all AppArmor profiles are in enforce mode

    `# aa-status`

2. if any profiles are in complain mode, set them to enforce after reloading

    `# sudo systemctl reload apparmor`

    `# aa-enforce /etc/apparmor.d/*`

### NetworkManager

1. remove any previous config in the /etc/network/interfaces file

    `# echo "" | tee /etc/network/interfaces`

2. also, disable the networking service

    `# systemctl disable networking --now`

3. make sure NetworkManager is enabled

    `$ systemctl status NetworkManager`

4. if not, enable it

    `# systemctl enable NetworkManager --now`

5. restart NetworkManager after disabling networking

    `# systemctl restart NetworkManager`

6. add a new connection

    `$ nmcli dev wifi connect <ssid> password <password>`

7. and, to enable WPA3 (dragonfly), 

    `$ nmcli con mod <ssid> wifi-sec.key-mgmt sae`

8. to use cloudflare as dns

    `$ nmcli con mod <ssid> ipv4.dns "1.1.1.1 1.0.0.1"`

9. to disable IPv6

    `$ nmcli con mod <ssid> ipv6.method disabled`

10. then restart NetworkManager

    `# systemctl restart NetworkManager`

### bluetooth

1. disable bluetooth daemon

    `# systemctl disable bluetooth --now`

2. edit the file /etc/bluetooth/main.conf to uncomment FastConnectable and set it to true

    `# sed -i '/^#FastConnectable/s/^#//; s/^FastConnectable.*$/FastConnectable = true/' /etc/bluetooth/main.conf`

3. uncomment ReconnectAttempts

    `# sed -i '/^#ReconnectAttempts/s/^#//;' /etc/bluetooth/main.conf`

4. uncomment ReconnectIntervals

    `# sed -i '/^#ReconnectIntervals/s/^#//;' /etc/bluetooth/main.conf`

### auto-cpufreq

1. once `auto-cpufreq` is installed, install the daemon

    `# auto-cpufreq --install`

### powertop

1. enable the powertop service

    `# systemctl enable powertop --now`

### cups

1. add user to lpadmin group

    `# usermod -aG lpadmin vrm`

2. make sure cups is enabled

    `$ systemctl status cups`

3. cups web interface is at localhost:631

### keyring

1. if a default keyring doesn't exist, create one called "login" using seahorse

    `$ seahorse`

2. edit /etc/pam.d/login to add these lines
    
    1. auth       optional     pam_gnome_keyring.so
    2. session    optional     pam_gnome_keyring.so auto_start
    ```
    # The PAM configuration file for the Shadow `login' service

    # ... (existing configuration)

    # Standard Un*x authentication.
    @include common-auth

    # Add the following line to enable gnome-keyring authentication
    auth       optional     pam_gnome_keyring.so  # ADD THIS

    # This allows certain extra groups to be granted to a user
    # based on things like time of day, tty, service, and user.
    # Please edit /etc/security/group.conf to fit your needs
    # (Replaces the `CONSOLE_GROUPS' option in login.defs)
    auth       optional   pam_group.so

    # Uncomment and edit /etc/security/time.conf if you need to set
    # time restraint on logins.
    # (Replaces the `PORTTIME_CHECKS_ENAB' option from login.defs
    # as well as /etc/porttime)
    # account    requisite  pam_time.so

    # ... (existing configuration)

    # Standard Un*x account and session
    @include common-account
    @include common-session

    # Add the following line to auto-start gnome-keyring in the session
    session    optional     pam_gnome_keyring.so auto_start  # ADD THIS

    # ... (existing configuration)

    ```

    or,

    `# sed -i '/^@include common-auth/a auth       optional     pam_gnome_keyring.so' /etc/pam.d/login`

    `# sed -i '/^@include common-session/a session    optional     pam_gnome_keyring.so auto_start' /etc/pam.d/login`

### root account

1. change the root shell from bash to nologin in the /etc/passwd file

    `# usermod -s /usr/sbin/nologin root`

### rust

1. install stable rust

    `$ rustup default stable`

2. verify that packages have been installed

    `$ rustc --version`

    `$ cargo --version`

    `$ rustfmt --version`

### timeshift

1. setup weekly snapshots, store 2
2. exclude `/home/vrm` and `/nix`

# rose config

## install

1. device: raspberry pi 4
2. os: rpi os lite 64 bit
3. other settings:
    1. hostname: rose
    2. username: vrm, set password
    3. configure wireless lan with country
    4. set local and keyboard layout
    5. enable ssh with public key authentication
    6. disable telemetry

## packages

### sources

all packages are from **apt**

### list of packages
```
ufw
micro
cryptsetup
xfsprogs
smartmontools
git
foot (for ssh from noir)
```

## additional config

### sudo

1. remove the sudo nopasswd file

    `# rm /etc/sudoers.d/010_pi-nopasswd`

### ssh

1. edit sshd_config to uncomment and change the port
	
### ufw

1. allow ssh connections to custom port from local IPs

    `# ufw allow from 192.168.0.0/24 to any port xxxx`

2. allow ports for syncthing on local IPs

	`# ufw allow from 192.168.0.0/24 to any port 8384`

	`# ufw allow from 192.168.0.0/24 to any port 22000`

	`# ufw allow from 192.168.0.0/24 to any port 21027`

2. enable ufw

    `# ufw enable`

3. check status

    `# ufw status verbose`

### NetworkManager

1. uses NetworkManager by default

2. edit the file in /etc/NetworkManager/system-connections/preconfigured.nmconnection

3. add the following lines, replace the existing ipv4 settings if necessary
    ```
    [ipv4]
    method=manual
    address1=192.168.0.xx/24
    gateway=192.168.0.1
    dns=192.168.0.1;
    ```

4. to use cloudflare as dns

    `# nmcli con mod "preconfigured" ipv4.dns "1.1.1.1 1.0.0.1"`

    5. to disable ipv6

    `# nmcli con mod "preconfigured" ipv6.method disabled`

5. then restart NetworkManager

    `# systemctl restart NetworkManager`

### cryptsetup
    
1. generate key

    `# dd if=/dev/urandom of=/root/keyfile bs=1024 count=4`

    `# chmod 0400 /root/keyfile`

2. format the disk with the key using LUKS

    `# cryptsetup luksFormat --type luks1 --key-file /root/keyfile /dev/sda`

3. mount encrypted disk

    `# cryptsetup luksOpen --key-file /root/keyfile /dev/sda drive`

4. format the disk

    `# mkfs.xfs /dev/mapper/drive`

5. mount the disk

    `# mount /dev/mapper/drive /mnt/drive`

6. edit crypttab and add this line

    `drive /dev/sda /root/keyfile luks`

7. edit fstab and add this line

    `/dev/mapper/drive /mnt/drive ext4 defaults`

8. create a service in /etc/systemd/system and add these lines
    ```
    [Unit]
    Description=Set ownership of /mnt/drive at startup
    After=network.target

    [Service]
    Type=oneshot
    ExecStart=/bin/chown -R vrm:vrm /mnt/drive

    [Install]
    WantedBy=multi-user.target

    ```
    
9. enable the service

    `# systemctl enable <service_name>.service`

10. update initramfs

    `# update-initramfs -u`

### syncthing

1. after installing syncthing, run it once to create config files

	`$ syncthing`

2. edit ~/.config/syncthing/config.xml and change the address of the gui
	```
	127.0.0.1:8384     [access only from rose]
	192.168.0.xx:8384  [access only on local network*]
	0.0.0.0:8384       [full access through internet]

	*not reliable; use ufw rules as well
	```
	
3. acess syncthing gui and change settings

	1. disable anonymous usage reporting
	2. set a password
	3. disable global discovery and relaying

4. edit ~/.config/syncthing/config.xml and in the gui section change tls to true

5. enable syncthing at startup

    `# systemctl enable syncthing@vrm --now`

# security

## noir

### attack surfaces

1. physical access
2. packages
3. user accounts
4. network
5. browser
6. passwords

### physical access

1. LUKS encryption is enabled for the boot drive with a strong, high entropy password
2. swap is also encrypted with a key from /dev/urandom
3. laptop has an admin password for bios
4. laptop has secure boot and tpm enabled and active

if an adversary were to obtain physical access to the device:

1. can not boot into the disk
2. can not make unauthorized changes to bios settings, such as booting from a different drive

### packages

#### apt & repositories
1. debian stable repositories are used, currently `Debian 12 (bookworm)` 
2. package sources are listed above, all core packages are installed from apt, to ensure stability and security
3. packages are kept up to date regularly
4. no new non-debian-stable repositories are to be added to apt
5. debian uses `AppArmor` by default and all profiles are set to `enforce`

#### nix
1. only some packages like `brave` and `vscodium` are installed using the nix package manager
2. nix is used for the following reasons
    1. apt does not have these packages, and installing them would require adding new non-debian repositories, which is a security risk
    2. a newer version which is unavailable in debian is required
3. the packages installed from nix are ONLY free and open source software
4. non-free apps like `spotify` and `discord` are to be used using the web interface instead, despite having packages in the nix package repositories
5. reason for using the currently installed nix packages:
    1. swayfx: not available in debian repos
    2. brave: not available in debian repos
    3. rustup: not available in debian repos
    4. vscodium: not available in debian repos
    5. fastfetch: not available in debian repos
    6. ags: not available in debian repos
    7. cliphist: not available in debian repos
    8. nixGLIntel: self-explanatory

#### from source
1. only one package, `auto-cpufreq` is compiled from source (github)
2. the project is open source, widely used and therefore deemed to be secure
3. this is available in nix, but due to the containerization-like nature of nix, using root-level applications is complicated (eg. `waydroid`, or in this case, `auto-cpufreq`)

#### future considerations
1. any future packages installed must align with these security considerations
2. for example `waydroid` could be installed from nix but due to requirements such as root-level access and opening ports in ufw, such packages may not be feasible for maintinaing security and stability
3. while this means that not all packages can be used, it also ensures a stable and secure system

### user accounts

1. single user system with a strong, high entropy password
2. root account is disabled during setup, and the root shell is set to `/usr/sbin/nologin`

### network

1. ufw is used for firewall, with default rules
    ```
    Status: active
    Logging: on (low)
    Default: deny (incoming), allow (outgoing), deny (routed)
    New profiles: skip
    ```
2. for future packages that need open ports (eg. `waydroid`), try to not use the package; if it is essential, take serious consideration before opening ports
3. ssh server is not enabled, no remote desktop capabilites TO noir, only FROM noir (as a client)
4. WPA3 security for connecting to a wireless network
5. cloudflare is used for dns server
6. ipv6 is disabled

### browser

1. an open source browser like `firefox` or `brave` is to be used
2. the current browser is `brave` with some privacy and security oriented settings
3. the extensions are given access only to what they need (site-specific), and the ones with more access (eg. `darkreader`) are open source
4. tracker and ad blocking: aggressive
5. upgrade connection to https: strict
6. fingerprinting blocking: enabled
7. third party cookies are blocked
8. cloudflare is used for dns server with secure dns enabled
9. shield lists
    1. EasyList Cookie
    2. Fanboy's Annoyances
    3. Fanboy's Social
    4. Fanboy's Anti-Newsletter
    5. Fanboy's Mobile Notifications
    6. Fanboy's Anti-chat Apps
    7. uBlock Annoyances
    8. Youtube Mobile Distractions
    9. Bypass Paywalls Clean Filters
    10. ABPIndo
    11. IndianList
    12. Brave Experimental Adblock Rules
10. PASSES THE EFF FINGERPRINT TEST
11. telemetry, brave ads, rewards, wallet disabled
12. duckduckgo is the default search engine
13. private mode with tor enabled
14. ZERO passwords are stored in browser
15. send do not track requests: enabled
16. ...and more

### passwords

1. all passwords are stored LOCALLY using keepassxc with a strong, high entropy master password
2. regular maintenance of existing passwords, with health checks and changes
3. the keepassxc encrypted file is also backed up to cloud
4. important accounts have multi-factor-authentication enabled with phone, authenticator app, etc
5. protonmail is used for social media, etc

## rose

### attack surfaces

1. physical access
2. packages
3. user accounts
4. network

### physical access

1. the drive used for any file share like syncthing/smb/git-over-ssh is encrypted using cryptsetup with a keyfile

### packages

1. only from apt with debian repositories, currently `Debian 12 (bookworm)` kept up to date regularly

### user accounts

1. single user system with a strong, high entropy password
2. root account is disabled during setup
3. the `010_pi-nopasswd` file is removed, so password is necessary for sudo

### network

1. this is the biggest attack surface for rose
2. ufw is enabled with custom rules for ssh connections to a custom port and for syncthing, only from local IPs
    ```
    Status: active
    Logging: on (low)
    Default: deny (incoming), allow (outgoing), disabled (routed)
    New profiles: skip

    To                         Action      From
    --                         ------      ----
    xxxx                       ALLOW IN    192.168.0.0/24            
    8384                       ALLOW IN    192.168.0.0/24            
    22000                      ALLOW IN    192.168.0.0/24            
    21027                      ALLOW IN    192.168.0.0/24 
    ```
3. ssh port is not the default (22), only public key authentication is allowed, password authentication is disabled, the private key is currently only on noir
4. cloudflare is used for dns server
5. ipv6 is disabled

## backups (only for noir)

backups are essential to ensure availability of important data

1. timeshift backups (thrice weekly) are enabled
2. home directory is managed using git, and backed up to rose using git-over-ssh
3. only the encrypted keepassxc passwords file is cloud backed

### git setup for home directory
1. to create a new bare repository on rose

    `[rose]$ git init --bare vrm.git`

2. to setup git on noir

    1. to initialize (for first setup)

        `[noir]$ git init`

    2. setup remote
    
        `[noir]$ git remote add rose ssh://rose:/mnt/drive/vrm.git`
    
    3. add these paths to `.gitignore`
        ```
        # downloads may contain large files
        downloads/

        # cache, virtual envs and temporary files
        .cache/
        .virtualenvs/
        .fontconfig/
        *.tmp

        # history files
        .bash_history
        .python_history
        .lesshst

        # nix related files
        .nix-channels
        .nix-defexpr/
        .nix-profile/
        .local/state/nix/

        # ssh private key
        .ssh/id_ed25519
        ```
    
    4. add these paths to `.gitattributes`
        ```        
        # encrypt all files
        * filter=git-crypt diff=git-crypt

        # ignore git files
        .gitattributes !filter !diff
        .gitignore !filter !diff

        # ignore setup files
        documents/setup/ !filter !diff

        # ignore kpxc file
        documents/passwords.kdbx !filter !diff
        ```

    5. to setup git-crypt (for first setup)

        1. initialize git-crypt in the repository
        
            `[noir]$ git-crypt init`

        2. to export the keyfile
        
            `[noir]$ git-crypt export-key /tmp/keyfile`
        
        3. remember to shred the keyfile after use

            `[noir]$ shred -u /tmp/keyfile`
        
        4. add .gitignore and .gitattributes to git

            `[noir]$ git add .gitignore .gitattributes`
        
        5. commit .gitignore and .gitattributes

            `[noir]$ git commit -m "added gitignore and gitattributes"`

    6. then add changed files, commit changes and push

        `[noir]$ git add .`

        `[noir]$ git commit -m "<message>"`

        `[noir]$ git push rose master`

# vms

vms are used for two reasons:
1. using other operating systems
2. using packages can not conveniently be installed on noir

all vms are based on `qemu` and managed using `virt-manager`

a base example vm setup includes:
1. a linux vm with a desktop environment (eg. xfce) and flatpak
2. a windows vm, activated using `https://github.com/massgravel/Microsoft-Activation-Scripts` with the qemu guest agent

## setup

1. install `qemu` and `virt-manager`

`# apt install qemu-kvm qemu-system qemu-utils libvirt-clients libvirt-daemon-system bridge-utils virtinst libvirt-daemon virt-manager -y`

2. setup networking

```
# virsh net-start default
# virsh net-autostart default
```

3. add user to required groups

```
# usermod -aG libvirt vrm
# usermod -aG libvirt-qemu vrm
# usermod -aG kvm vrm
# usermod -aG input vrm
# usermod -aG disk vrm
```
