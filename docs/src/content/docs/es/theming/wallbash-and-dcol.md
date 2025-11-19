---
title: Wallbash y dcol
description: Entendiendo Wallbash y dcol
---

## Descripción general

Este documento proporciona una explicación de la configuración de colores utilizada para la creación de temas en HyDE. Abarca colores primarios, colores de texto y colores de acento. Cada color puede especificarse en formato hexadecimal o RGBA.

## Identificadores de color

Por defecto, durante el **almacenamiento en caché de fondos de pantalla**, se producirán 4 colores primarios, 4 colores de texto y 9 colores de acento para cada color primario.

- **`dcol_mode`**: Este identificador determina si el tema está en modo oscuro o claro.
- **`dcol_pryX`**: Estos son los colores primarios, donde `X` varía de 1 a 4.
- **`dcol_txtX`**: Estos son los colores primarios invertidos utilizados para texto, donde `X` varía de 1 a 4.
- **`dcol_XaxY`**: Estos son los colores de acento para cada color primario, donde `X` varía de 1 a 4 e `Y` varía de 1 a 9.
- **`_rgba`**: Este sufijo indica que el color está en formato RGBA. Si el sufijo no está presente, el color está en formato hexadecimal.
- **`_rgb`**: Este sufijo indica que el color está en formato RGB.

## Uso

Para utilizar la configuración de colores en caché:

1. Reemplaza el prefijo `dcol_` con `wallbash_` para permitir que el script Wallbash analice y cambie los valores.
2. Considera el prefijo `wallbash_` como un marcador de posición para el valor de color dominante.
3. Envuelve el identificador de color con corchetes angulares (`<...>`) para indicar el reemplazo con el valor correspondiente, p. ej., `<wallbash_pry1>`.
4. Usa este [ejemplo](https://github.com/hyde-project/hyde/tree/master/Configs/.config/hyde/wallbash) como plantilla.

Esto te permite crear una plantilla para configuraciones, utilizando el color dominante o fondo de pantalla, y dejar que el script Wallbash lo convierta por ti.

### Creando una plantilla `*.dcol`

Una plantilla requiere tres partes:

- Archivo de destino
- Script/comando (opcional)
- Contenidos

## El formato básico:

| destino      | comando |
| ------------ | ------- |
| **contenidos** |

---

> **Nota:** **destino**|**comando** siempre debe estar en la línea 1 de cada archivo de plantilla. La llamaremos `línea de encabezado`.

#### Archivo de destino

Estructura tu plantilla y determina la ubicación de configuración de destino. Esto puede ser:

- `${cacheDir}/wallbash` con post-procesamiento utilizando un script.
- Una ruta esperada, p. ej., junto a `kitty.conf` para Kitty, importada mediante `include theme.conf`.

Utiliza variables de entorno para manejar directorios de forma dinámica:

- `${confDir}` = `$XDG_CONFIG_HOME` o `$HOME/.config/`
- `${cacheDir}/wallbash` = `HYDE_CACHE_DIR/wallbash` = `$HOME/.cache/hyde`

#### Script/comando opcional

Después de llenar el archivo de destino con contenidos, puedes ejecutar comandos/scripts arbitrarios para post-procesamiento. Utiliza la variable `WALLBASH_SCRIPTS` para navegar al directorio de scripts de Wallbash, p. ej., `WALLBASH_SCRIPTS/tu_script.sh`.

> **Precaución:** Solo agrega plantillas de autores confiables para evitar ejecutar código malicioso.

#### Contenidos

Estos son los contenidos del archivo, que contienen marcadores de posición de Wallbash, p. ej., `<wallbash_pry1>`.

---

El directorio `~/.config/hyde/wallbash/*` contiene tres directorios principales:

### always

Las plantillas en `./wallbash/always/` se ejecutan durante:

- Cambio de tema
- Cambio de fondo de pantalla
- Cambio de modo

Más información [aquí](./always/README).

### theme

Las plantillas en `./wallbash/theme/` se ejecutan durante:

- Cambio de tema
- Cambio de modo

Más información [aquí](./theme/README).

### scripts

Para personalización, almacena tus scripts en `./wallbash/scripts`. Utiliza la variable `$WALLBASH_SCRIPTS` para navegar por este directorio.