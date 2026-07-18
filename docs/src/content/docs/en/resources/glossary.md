---
title: Glossary
description: Key terms used in Tsumiki documentation
---

A quick reference for terms used across the Tsumiki docs.

## Widget

A small, self-contained UI element on the panel (for example, clock, battery, volume). Widgets are configured under `[widgets.<name>]` in `config.toml`.

## Module

A larger UI surface beyond the bar, such as the dock, notifications, overview, OSD, or the bar itself. Modules are enabled under `[modules.<name>]`.

## Layout

Defines where widgets appear on the bar through `left_section`, `middle_section`, and `right_section` lists.

## Theme

A set of color variables defined in `themes/*.toml` and consumed by SCSS during style compilation.

## Matugen

A tool that generates Material You color palettes from a wallpaper image. See [Theming with Matugen](/en/theming/matugen).

## Fabric

The widget system Tsumiki is built on, providing the UI primitives and event model.

## Collapsible Group

A group of widgets hidden behind a single toggle, defined with `[[collapsible_groups]]` in `config.toml`.

## Widget Group

A named collection of widgets with shared spacing and style classes, defined with `[[widget_groups]]`.
