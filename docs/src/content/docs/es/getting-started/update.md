---
title: Actualización
description: Guía de gestión de HyDE Dotfiles
---

## Automatizada

Para actualizar HyDE, necesitarás obtener los últimos cambios de GitHub y restaurar las configuraciones ejecutando los siguientes comandos:

```shell
cd ~/HyDE/Scripts
git pull origin master
./install.sh -r
```

:::note

Cualquier configuración que hayas realizado será sobrescrita si está listada para serlo según `Scripts/restore_cfg.psv`.
Sin embargo, todas las configuraciones reemplazadas están respaldadas y pueden recuperarse desde `~/.config/cfg_backups`.
Consulta [Restaurar Configuración](/hyde/installation/restore/) para más información.

:::

## Actualización avanzada y manual

Además del comando anterior, puedes modificar el archivo [Scripts/restore_cfg.psv](https://github.com/HyDE-Project/HyDE/blob/master/Scripts/restore_cfg.psv). La documentación se encuentra en el archivo.

También consulta [esto](../resources/restore.md).

### Actualizar SOLO los dotfiles

:::note

> "restore" en este contexto significa restaurar los dotfiles desde el repositorio a tu $HOME, no al revés.

```sh
./restore_cfg.sh </ruta/al/archivo.psv> <opcional /ruta/al/clon/de/hyde>
```

:::

<details>
<summary>Más como esto</summary>

```sh
cd ~/HyDE/Scripts
./restore_cfg.sh ./restore_cfg.psv
```

</details>

---
