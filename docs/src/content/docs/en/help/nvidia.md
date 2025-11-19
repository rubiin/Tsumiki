---
title: NVIDIA
description: For NVIDIA GPU users
---

HyDE's installation automates the installation of **NVIDIA drivers** and **nvidia-utils**.

:::note
More information at: https://wiki.archlinux.org/title/NVIDIA

:::

This table shows what drivers will be added to your system based on the nvidia GPU you have.

<!-- START TABLE OF CONTENTS -->

# Table of Contents

- [nvidia-340xx-dkms](#nvidia-340xx-dkms)
- [nvidia-390xx-dkms](#nvidia-390xx-dkms)
- [nvidia-470xx-dkms](#nvidia-470xx-dkms)
- [nvidia-dkms](#nvidia-dkms)
<!-- END TABLE OF CONTENTS -->

<!-- START NVIDIA TABLE -->

## nvidia-340xx-dkms

| NVE0 | NVE4 | GK104 | Description                                                                                                                                                                                                                                                  |
| ---- | ---- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| NV50 | NV50 | G80   | GeForce 8800 (GTS, GTX, Ultra), Quadro FX (4600 (SDI), 5600)                                                                                                                                                                                                 |
| NV50 | NV84 | G84   | GeForce 8600 (GT, GTS, M GT, M GS), 8700M GT, GeForce 9500M GS, 9650M GS, Quadro FX (370, 570, 570M, 1600M, 1700), NVS 320M                                                                                                                                  |
| NV50 | NV86 | G86   | GeForce 8300 GS, 8400 (GS, M G, M GS, M GT), 8500 GT, GeForce 9300M G, Quadro FX 360M, NVS (130M, 135M, 140M, 290)                                                                                                                                           |
| NV50 | NV92 | G92   | GeForce 8800 (GT, GS, GTS 512, M GTS, M GTX), GeForce 9600 GSO, 9800 (GT, GTX, GTX+, GX2, M GT, M GTX), GeForce GTS 150(M), GTS 160M, GTS 240, GTS 250, GTX (260M, 280M, 285M), GT (330, 340), Quadro FX (2800M, 3600M, 3700, 3700M, 3800M, 4700 X2), VX 200 |
| NV50 | NV94 | G94   | GeForce 9600 (GSO 512, GT, S), 9700M GTS, 9800M GTS, GeForce G 110M, GT 130(M), GT 140, Quadro FX (1800, 2700M)                                                                                                                                              |
| NV50 | NV96 | G96   | GeForce 9400 GT, 9500 (GT, M G), 9600 (M GS, M GT), 9650M GT, 9700M GT, GeForce G 102M, GT 120, Quadro FX (380, 580, 770M, 1700M)                                                                                                                            |
| NV50 | NV98 | G98   | GeForce 8400 GS, GeForce 9200M GS, 9300 (GE, GS, M GS), GeForce G 100, G 105M, Quadro FX (370 LP, 370M), NVS (150M, 160M, 295, 420, 450)                                                                                                                     |
| NV50 | NVA0 | GT200 | GeForce GTX (260, 275, 280, 285, 295), Quadro CX, FX (3800, 4800, 5800)                                                                                                                                                                                      |
| NV50 | NVA3 | GT215 | GeForce GT (240, 320, 335M), GTS (250M, 260M, 350M, 360M), Quadro FX 1800M                                                                                                                                                                                   |
| NV50 | NVA5 | GT216 | GeForce GT (220, 230M, 240M, 325M, 330M), 315, Quadro 400, FX 880M, NVS 5100M                                                                                                                                                                                |
| NV50 | NVA8 | GT218 | GeForce 8400 GS, ION 2, GeForce 205, 210, G 210M, 305M, 310(M), 405, Quadro FX (380 LP, 380M), NVS (300, 2100M, 3100M)                                                                                                                                       |
| NV50 | NVAA | MCP77 | GeForce 8100, 8200, 8300 mGPU                                                                                                                                                                                                                                |
| NV50 | NVAA | MCP78 | nForce 700a series, 8200M G                                                                                                                                                                                                                                  |
| NV50 | NVAC | MCP79 | ION, GeForce 9300, 9400 mGPU                                                                                                                                                                                                                                 |
| NV50 | NVAC | MCP7A | nForce 700i series, 8200M G, 9100M, 9400M (G)                                                                                                                                                                                                                |
| NV50 | NVAF | MCP89 | GeForce 320M                                                                                                                                                                                                                                                 |

## nvidia-390xx-dkms

| NVE0 | NVE4 | GK104 | Description                                                                                                                   |
| ---- | ---- | ----- | ----------------------------------------------------------------------------------------------------------------------------- |
| NVC0 | NVC0 | GF100 | GeForce GTX (465, 470, 480, 480M), Quadro 4000, 5000[M] (??), 6000                                                            |
| NVC0 | NVC1 | GF108 | GeForce GT (415M, 420, 420M, 425M, 430, 435M, 520M, 525M, 530, 540M, 550M, 555M, 620, 630M, 635M, 640M LE), Quadro 600, 1000M |
| NVC0 | NVC3 | GF106 | GeForce GT (440, 445M, 545, 555M, 630M, 635M), GTS 450, GTX 460M, Quadro 2000 (D), 2000M                                      |
| NVC0 | NVC4 | GF104 | GeForce GTX (460, 460 SE, 470M, 485M), Quadro 5000M (??)                                                                      |
| NVC0 | NVC8 | GF110 | GeForce GTX (560 Ti OEM, 570, 580, 590), Quadro 3000M, 4000M, 5010M                                                           |
| NVC0 | NVCE | GF114 | GeForce GTX (460 v2, 560, 560 Ti, 570M, 580M, 670M, 675M)                                                                     |
| NVC0 | NVCF | GF116 | GeForce GTS 450 v2, GTX (550 Ti, 560M)                                                                                        |
| NVC0 | NVD7 | GF117 | Geforce GT 620M, 625M, (some) 630M, 710M, 720M                                                                                |
| NVC0 | NVD9 | GF119 | GeForce 410M, 510 (?), GT (520, 520M, 520MX, 610), 610M, Quadro NVS 4200M                                                     |

## nvidia-470xx-dkms

| NVE0 | NVE4  | GK104  | Description                                                                                                                                                        |
| ---- | ----- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| NVE0 | NVE4  | GK104  | GeForce GTX (660 Ti, 670[M], 680[M], 690, 760, 760 Ti, 770, 775M, 780M, 860M), Quadro K3000[M], K3100M, K4000[M], K4100[M], K5000[M], K5100M, Tesla K10            |
| NVE0 | NVE7  | GK107  | GeForce GT (640[M], 645M, 650M, 710M, 720M, 730M, 740[M], 745M, 750M, 755M), GTX (650, 660M), Quadro 410, K500[M], K600, K1000[M], K1100M, K2000[M], NVS 510, 1000 |
| NVE0 | NVE6  | GK106  | GeForce GTX (645, 650 Ti, 660, 760M, 765M, 770M), Quadro K2100M, K4000                                                                                             |
| NVE0 | NVF0  | GK110  | GeForce GTX 780, Titan, Tesla K20, Quadro K6000                                                                                                                    |
| NVE0 | NVF1  | GK110B | GeForce GTX 780 Ti, Titan Z, Tesla K40                                                                                                                             |
| NVE0 | NV106 | GK208B | GeForce GT 720                                                                                                                                                     |
| NVE0 | NV108 | GK208  | GeForce GT 630, 635, 640, 710M, 720M, 730M, 735M, 740M, 920M, Quadro K510M, K610M                                                                                  |
| NVE0 | NVEA  | GK20A  | Tegra K1                                                                                                                                                           |
| NVE0 | NV??? | GK210  | Tesla K80                                                                                                                                                          |

## nvidia-dkms

| NVE0  | NVE4  | GK104 | Description                                                                                                                 |
| ----- | ----- | ----- | --------------------------------------------------------------------------------------------------------------------------- |
| NV110 | NV117 | GM107 | GeForce GTX (745, 750, 750 Ti, 840M, 845M, 850M, 860M, 950M, 960M) Quadro K620, K1200, K2200, M1000M, M1200M; GRID M30, M40 |
| NV110 | NV118 | GM108 | GeForce 830M, 840M, 930M, 940M[X]                                                                                           |
| NV110 | NV120 | GM200 | GeForce GTX Titan X                                                                                                         |
| NV110 | NV124 | GM204 | GeForce GTX (970, 980)                                                                                                      |
| NV110 | NV126 | GM206 | GeForce GTX (950, 960)                                                                                                      |
| NV110 | NV12B | GM20B | Tegra X1                                                                                                                    |
| NV130 | NV132 | GP102 | NVIDIA Titan (X, Xp), GeForce GTX 1080 Ti                                                                                   |
| NV130 | NV134 | GP104 | GeForce GTX (1070, 1080)                                                                                                    |
| NV130 | NV136 | GP106 | GeForce GTX 1060                                                                                                            |
| NV130 | NV137 | GP107 | GeForce GTX (1050, 1050 Ti)                                                                                                 |
| NV130 | NV138 | GP108 | GeForce GT 1030                                                                                                             |
| NV140 | NV140 | GV100 | NVIDIA Titan V, NVIDIA Quadro GV100                                                                                         |
| NV160 | NV162 | TU102 | NVIDIA Titan RTX, GeForce RTX 2080 Ti                                                                                       |
| NV160 | NV164 | TU104 | GeForce RTX (2070 Super, 2080, 2080 Super)                                                                                  |
| NV160 | NV166 | TU106 | GeForce RTX (2060, 2060 Super, 2070)                                                                                        |
| NV160 | NV168 | TU116 | GeForce GTX (1650 Super, 1660, 1660 Ti, 1660 Super)                                                                         |
| NV160 | NV167 | TU117 | GeForce GTX 1650                                                                                                            |
| NV170 | NV172 | GA102 | GeForce RTX (3080, 3090)                                                                                                    |
| NV170 | NV174 | GA104 | GeForce RTX (3060 Ti, 3070, 3080 Mobile)                                                                                    |
| NV170 | NV176 | GA106 | GeForce RTX (3050, 3060)                                                                                                    |
| NV170 | NV177 | GA107 | GeForce RTX 3050                                                                                                            |
| NV190 | NV192 | AD102 | GeForce RTX 4090                                                                                                            |
| NV190 | NV193 | AD103 | GeForce RTX 4080                                                                                                            |
| NV190 | NV194 | AD104 | GeForce RTX (4070, 4070 Ti)                                                                                                 |
| NV190 | NV196 | AD106 | GeForce RTX 4060 Ti                                                                                                         |
| NV190 | NV197 | AD107 | GeForce RTX 4060                                                                                                            |

<!-- END NVIDIA TABLE -->

:::note

:::
