---
title: Instalación
description: Guía de instalación de HyDE
---

El script de instalación está diseñado para una instalación mínima de [Arch Linux](https://wiki.archlinux.org/title/Arch_Linux), pero **puede** funcionar en algunas distribuciones [basadas en Arch](https://wiki.archlinux.org/title/Arch-based_distributions).
Aunque la instalación de HyDE junto con otro entorno de escritorio [(DE)](https://wiki.archlinux.org/title/Desktop_environment) o gestor de ventanas [(WM)](https://wiki.archlinux.org/title/Window_manager) debería funcionar, al ser una configuración altamente personalizada, **podría** haber conflictos con tu tema de [GTK](https://wiki.archlinux.org/title/GTK)/[Qt](https://wiki.archlinux.org/title/Qt), [Shell](https://wiki.archlinux.org/title/Command-line_shell), [SDDM](https://wiki.archlinux.org/title/SDDM), [GRUB](https://wiki.archlinux.org/title/GRUB), etc. Lo haces bajo tu propio riesgo.

Para NixOS, hay un proyecto independiente que se mantiene en @ [Hydenix](https://github.com/richen604/hydenix/tree/main)

:::note

El script de instalación detectará automáticamente una tarjeta gráfica NVIDIA e instalará los controladores nvidia-dkms para tu kernel.
Asegúrate de que tu tarjeta gráfica NVIDIA sea compatible con los controladores dkms en la lista proporcionada [aquí](https://wiki.archlinux.org/title/NVIDIA).

:::danger

El script modifica tu configuración de `grub` o `systemd-boot` para habilitar NVIDIA DRM (Direct Rendering Manager).

:::

<!-- ### Option 1 -->

### Script de instalación automática

```shell
pacman -S --needed git base-devel
git clone --depth 1 https://github.com/HyDE-Project/HyDE ~/HyDE
cd ~/HyDE/Scripts
./install.sh
```

:::tip
También puedes agregar cualquier otra aplicación que desees instalar junto con HyDE em `Scripts/pkg_user.lst` y pasar el archivo como parámetro para instalarlo así:

```shell
./install.sh pkg_user.lst
```

:::

:::note
Consulta tu lista desde `Scripts/pkg_extra.lst`
O puedes ejecutar `cp  Scripts/pkg_extra.lst Scripts/pkg_user.lst` si deseas instalar los paquetes extra.
:::

### Instalación avanzada y manual

#### Clonar

Clona el repositorio y cambia al directorio del script. Asegúrate de que el usuario tenga permisos de [e]scritura y e[j]ecución en el directorio clonado:

```sh
pacman -Sy git
git clone --depth 1 https://github.com/prasanthrangan/hyprdots ~/HyDE
cd ~/HyDE/Scripts
```

:::caution
**NUNCA** ejecutes el script con sudo ni como usuario root!
:::

#### Modos

El script de instalación puede ejecutarse en diferentes modos:

- Para una instalación completa por defecto de Hyprland con todas las configuraciones:

```shell
./install.sh
```

- Para una instalación completa o mínima de Hyprland más tus paquetes favoritos (ej.`pkg_user.lst`)

```shell
./install.sh pkg_user.lst # instalación completa: pkg_core.lst + pkg_user.lst con configuraciones
./install.sh -i pkg_user.lst # instalación mínima: pkg_core.lst + pkg_user.lst sin configuraciones
```

- Cada [sección](#process) también puede ejecutarse de forma independiente:

```shell
./install.sh -i # instalación mínima de Hyprland sin configuraciones
./install.sh -d # instalación mínima sin configuraciones, pero con instalación (--noconfirm)
./install.sh -r # solo restaura los archivos de configuración
./install.sh -s # inicia y habilita los servicios del sistema
./install.sh -t # prueba sin ejecutar (modo simulación -irst)
./install.sh -m # omite la instalación del tema
./install.sh -n # omite la instalación de los controladores NVIDIA
./install.sh -irst # realiza una prueba (dry run) de todo
```

<!-- ### Option 2

:::caution

HyDE-CLI author here.
The CLI's dots management (Hyde {restore,backup,control,override}) is not yet and might not be 100% compatible of the current hyprdots.
This is due to incompatibility of the meta files
and the above commands need manual intervention
Rest assured that other commands are working perfectly
and will be ported to its own `hydectl` command line interface

:::

As a second install option, you can also use `Hyde-install`, which might be easier for some.
View installation instructions for HyDE in [Hyde-cli - Usage](https://github.com/kRHYME7/Hyde-cli?tab=readme-ov-file#usage).

### Option 3

...Soon
A declarative way to manage importing and exporting dotfiles from other users. This is not for boot strapping but for sharing dotfiles.

---

---

---

:::note

> Please reboot after the install script completes and takes you to the SDDM login screen (or black screen) for the first time.
> ::: -->
