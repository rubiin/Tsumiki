---
title: Preguntas Frecuentes
description: Preguntas frecuentes sobre Tsumiki
---

:::tip
Para comportamiento específico de Hyprland, consulta la [Wiki de Hyprland](https://wiki.hyprland.org).
:::

<details>
<summary id="system-tray">¿No puedes ver la bandeja del sistema?</summary>
<div>

Puede que otra barra aún esté ejecutándose. Detenla primero:

```sh
pkill nombre-barra
```

</div>
</details>

<details>
<summary id="notifications">¿No puedes ver las notificaciones?</summary>
<div>

Otro daemon de notificaciones puede estar manejando las notificaciones. Detén los daemons comunes:

```sh
pkill -f "mako|dunst|waybar"
```

</div>
</details>

<details>
<summary id="bar">¿No puedes ver la barra?</summary>
<div>

Reinicia Tsumiki desde la raíz del proyecto e inspecciona la salida:

```sh
pkill tsumiki
tsu -start
```

Si ves `ModuleNotFoundError`, instala las dependencias:

```sh
uv sync
```

Si el problema continúa, abre un issue e incluye los registros.

</div>
</details>

<details>
<summary id="sass-error">¿Error de compilación Sass o la UI no se renderiza?</summary>
<div>

Tu `config.toml` puede estar desactualizado o ser inválido. Restablécela desde el ejemplo:

```sh
cp example/config.toml config.toml
```

Esto sobrescribe los valores personalizados.

</div>
</details>

<details>
<summary id="no-icons">¿Sin iconos?</summary>
<div>

Usa un tema de iconos con amplia cobertura. `Tela Circle` es una opción común.

</div>
</details>

<details>
<summary id="import-error">ImportError: no se puede importar XX</summary>
<div>

Esto generalmente significa que falta una dependencia requerida.

Instala las dependencias de ejecución y Python:

```sh
tsu -setup
```

o:

```sh
uv sync
```

</div>
</details>

<details>
<summary id="blur-effects">¿Cómo activar el desenfoque y los efectos?</summary>
<div>

Añade estas entradas `layerrule` a `hyprland.conf`:

```sh
layerrule = blur, ^tsumiki-notifications$
layerrule = xray 0, ^tsumiki-notifications$
layerrule = blurpopups, ^tsumiki-notifications$
layerrule = ignorezero, ^tsumiki-notifications$
layerrule = noanim , ^tsumiki-notifications$
layerrule = blur, ^fabric$
layerrule = ignorezero, ^fabric$
layerrule = xray 0, ^fabric$
layerrule = blurpopups, ^fabric$
layerrule = blur, ^tsumiki$
layerrule = xray 0, ^tsumiki$
layerrule = blurpopups, ^tsumiki$
layerrule = ignorezero, ^tsumiki$
layerrule = blur ,gtk-layer-shell
layerrule = ignorezero ,gtk-layer-shell
layerrule = blur, ^launcher$
layerrule = xray 0, ^launcher$
layerrule = blurpopups, ^launcher$
layerrule = ignorezero, ^launcher$
layerrule = animation popin, ^launcher$
```

</div>
</details>

<details>
<summary id="updating">¿Cómo actualizo Tsumiki?</summary>
<div>

Haz pull de los últimos cambios:

```sh
cd ~/.config/tsumiki
git pull
```

:::note
Mantén una copia de seguridad de `config.toml` antes de actualizaciones importantes.
:::

</div>
</details>
