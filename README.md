# FabricPanel

A semi-customizable bar written using the [Fabric Widget System](https://github.com/Fabric-Development/fabric)  
For installation and getting started with dependencies, refer to the [Fabric Wiki Installation Guide](https://its-darsh.github.io/fabric-wiki/introduction/installation-guide/).

---

## **Prerequisites**

- **JetBrains Nerd Font**

---

## **Installation**

### **1. Install Dependencies**

Run the following command to install the required packages:

```bash
# Arch Linux

sudo pacman -S gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python python-pip python-gobject python-cairo python-loguru pkgconf

# OpenSUSE

sudo zypper install gtk3-devel cairo-devel gtk-layer-shell-devel libgirepository-1_0-1 libgirepository-2_0-0 gobject-introspection-devel python311 python311-pip python311-gobject python311-gobject-cairo python311-pycairo python311-loguru pkgconf
```

### **2. Clone the Repository**

Clone this repository:

```bash
git clone https://github.com/rubiin/FabricPanel.git
cd FabricPanel
```

### **3. Install Dependencies**

Install the requirements:

```
pip install -r requirements.txt
```

---

## **Usage**

### **For Hyprland:**

Add the following line to your `hypr.conf` to start FabricPanel automatically:

```bash
exec = python main.py
```

### **For Other Window Managers:**

Use a similar configuration for your respective window manager's autostart setup.

> [!WARNING]
> This is still in early development and will include breaking changes
