`hid-nx` Linux kernel HID driver for Nintendo Switch controllers
================================================================

This repository contains the source code for a Linux kernel module called `hid-nx`. This module is an [HID](https://en.wikipedia.org/wiki/Human_interface_device) driver for the Nintendo Switch controllers.

The `hid-nx` driver module is meant to be used in place of the in-kernel `hid-nintendo` driver. `hid-nx` provides equivalent functionality and [extends support to the Nintendo Switch Online controllers](#supported-controllers).

For more information about the differences between this and the `hid-nintendo` driver included in the Linux kernel, see the ["History" section](#history) further down.

About this fork
---------------

I've been exploring Fedora Silverblue as an immutable distro alternative for it to become my daily driver. As I've used this driver in the past, I wanted to install it there, but the immutable nature of Silverblue makes it (at least for now) incompatible with DKMS, so I needed to add akmods support for it to work.

I've been working on it during a few days, and managed to create working packages with akmods instead of DKMS.

After some rigorous testing (playing TLOZ with the N64 controller) and some kernel updates in between, it was finally time to contribute with this changes to add akmods support.


Source
------

The [original source code](https://github.com/emilyst/hid-nx-dkms) was written by [emilyst](https://github.com/emilyst), and [this version](https://github.com/mlucianoeze/hid-nx) is a fork that supports akmods in addition to DKMS.


Status
------

This driver should be considered **experimental**.

It ought to be stable enough for day-to-day use. However, its supported features, input mappings, device names, and so on may still be subject to change. Please read this document carefully if you experience any issues.

It is my eventual goal to propose some of these changes to the in-kernel driver, but no proposal is currently in progress.


Supported controllers
---------------------

This driver continues to support devices implemented by the original `hid-nintendo` driver:

* Nintendo Switch Joy-Cons (separately, [together](#combining-joy-con-devices), or in a charging grip)
* Nintendo Switch Pro Controller

This driver also supports these Nintendo Switch Online controllers:

* [SNES controller for Nintendo Switch Online](https://www.nintendo.com/store/products/super-nintendo-entertainment-system-controller/)
* [NES Joy-Con controllers for Nintendo Switch Online](https://www.nintendo.com/store/products/nintendo-entertainment-system-controllers/)
* [Sega Genesis control pad for Nintendo Switch Online](https://www.nintendo.com/store/products/sega-genesis-control-pad/)
* [Nintendo 64 controller for Nintendo Switch Online](https://www.nintendo.com/store/products/nintendo-64-controller/)

This does **not** include controllers for the "Classic" consoles released by Nintendo.

> **Note**: Compared to `hid-nintendo`, devices using the `hid-nx` driver module will have the following different behaviors:
>
> * Input mappings: During refactoring to more easily accommodate adding new device inputs, the ordering and mapping of some inputs were rearranged for existing controllers for consistency.
> * Device names: Rather than hard-code names per device, as in the mainline driver, it's allowed for each device to report its own name on connection. This means the device's name differs slightly in some cases, as seen in programs like GNOME's Bluetooth settings, or RetroArch.
>   * Unfortunately, RetroArch configures controllers by device name, and this means some controllers will no longer be automatically configured by RetroArch when using this driver. There is hope that in the future, useful autoconfiguration files will be supplied for use, but in the meantime, you will need to configure those controllers' inputs manually.
>   * This should not impact Joy-Cons, use of `joycond`, etc.


Supported Linux kernel versions
-------------------------------

This driver should work with Linux kernel versions 5.16 or greater (the same kernel version in which the `hid-nintendo` driver appeared).

It may work on earlier versions, but they are not supported.


Installation
------------

If you are installing on Arch Linux, this driver [can be built and installed as a package](#as-a-package-on-arch-linux). This is recommended.

If you are using a Red Hat-based distribution such as Fedora, you can [download and install the RPM packages](#as-an-rpm-package-for-red-hat-based-distributions), or even [build your own packages from source](#building-rpm-packages-from-source) as well.

Otherwise, [see the DKMS installation instructions](#from-source-using-dkms).

Once installed, this driver replaces the native `hid-nintendo` driver. No other configuration should be necessary.

DKMS and akmods will automatically rebuild the driver for every kernel you install in the future.


### As a package on Arch Linux

On Arch Linux, instead of installing from source directly, it is possible to build and install the module as a package. This is helpful because the Pacman packaging system will be aware of it. (Note, though, that even if you install as a package, the [DKMS](https://wiki.archlinux.org/title/Dynamic_Kernel_Module_Support) system is still used to manage the module.)

Run the following command *without* using root permissions. Once the package is built, you will be asked to confirm and authenticate for the package installation.

    makepkg --clean --cleanbuild --syncdeps --force --install


### As an RPM package for Red Hat-based distributions

On Red Hat-based distributions such as Fedora (an its atomic variants such as Silverblue, Kinoite, etc.), instead of installing from source directly, it is possible to install the module as a package. This is helpful because the rpm packaging system will be aware of it. (Note that the [akmod](https://rpmfusion.org/Packaging/KernelModules/Akmods) system will be used to manage the module.)

This module consists of two packages: `akmod-hid-nx` and `hid-nx-kmod-common`. They are both installed together, as they depend on each other.

You can download them from the [Releases](https://github.com/mlucianoeze/hid-nx/releases) page, or [build them from source](#building-rpm-packages-from-source).

Install using `dnf`:

    sudo dnf install ./path/to/akmod-hid-nx.rpm ./path/to/hid-nx-kmod-common.rpm

Install using `rpm-ostree`:

    rpm-ostree install ./path/to/akmod-hid-nx.rpm ./path/to/hid-nx-kmod-common.rpm


#### Building RPM packages from source

You will need some dependencies, such as `rpmdevtools` and `akmods`.

Run the following command *without* using root permissions, for it to create the file tree you need to build RPM packages if not present. This will be placed in your home directory.

    rpmdev-setuptree

Place the source of this repository in a folder named `hid-nx-${version}` (for example `hid-nx-1.14`), and tar that folder in a file with the same name `hid-nx-${version}.tar.gz`. Then move the tar file to `~/rpmbuild/SOURCES/`.

You can now cd into the source root directory, and run the following commands *without* root permissions.

    rpmbuild -ba ./hid-nx-kmod.spec
    rpmbuild -ba ./hid-nx-kmod-common.spec

After these commands are complete, both rpm files will be placed in `~/rpmbuild/RPMS/`. You will need to install the `akmod` package and the `common` package together, as described above.


### From source using DKMS

To install this driver from source on Linux, use [DKMS](https://github.com/dell/dkms). The process is described below.

Before installation, you should install DKMS support. Depending on which Linux distribution you use, you can run one of the following commands as root or using `sudo`:

* On Debian, Ubuntu, or Mint:   `apt-get install dkms`
* On Fedora:                    `dnf install dkms`
* On Arch Linux:                `pacman -S dkms`

Next, clone the source code.

    git clone https://github.com/mlucianoeze/hid-nx
    cd hid-nx

Then run the following commands as root or using `sudo`.

    dkms add .
    dkms build hid-nx/1.14
    dkms install hid-nx/1.14


Uninstallation
--------------

If you have installed this driver as a package, you can remove it using your package manager.

If you have instead installed it from source using DKMS, run the following commands as root or using `sudo` to remove fully.

    modprobe -r hid_nx
    dkms uninstall hid-nx/1.14
    dkms remove hid-nx/1.14
    rm -rf /usr/src/hid-nx-*


Combining Joy-Con devices
-------------------------

Neither the `hid-nintendo` driver nor the `hid-nx` driver will present two connected Joy-Con controllers as a single device on their own. A userspace daemon called [`joycond`](https://github.com/DanielOgorchock/joycond) provides this functionality. Install it and follow its instructions.

Arch Linux users can install [`joycond-git` from the Arch Linux User Repository](https://aur.archlinux.org/packages/joycond-git).

At this time, [I recommend adding workaround udev rules](99-joycond-ignore.rules) to prevent `joycond` from interacting with the NSO controllers. The file [`99-joycond-ignore.rules`](99-joycond-ignore.rules) implements these rules. Run as root:

    cp 99-joycond-ignore.rules /etc/udev/rules.d/
    udevadm control --reload


Planned
-------

* Refactors to break apart longer functions
* Possible ideas from `linux-rt`:
  * Replace kernel spinlocks with mutexes that support priority inheritance
  * Move all interrupt and software interrupts to kernel threads
* Possibly add more `unlikely` macros to error conditions
* Amend commits to add `Signed-Off-By` for my own work


History
-------

### Original work by [emilyst](https://github.com/emilyst)

This driver was originally taken from the source code [from `drivers/hid/hid-nintendo.c` at Linux kernel commit `3e732ebf7316ac83e8562db7e64cc68aec390a18`](https://github.com/torvalds/linux/blob/3e732). That driver source was first written by Daniel Ogorchock. [His Linux kernel fork can be found on GitHub.](https://github.com/DanielOgorchock/linux)

I then manually incorporated [changes from Nadia Holmquist Pedersen to support SNES and NES controllers from Nintendo Switch Online](https://github.com/nadiaholmquist/linux/tree/hid-nintendo).

After that, I extended this support to the Sega Genesis gamepad and [proposed it as a change to Daniel's tree](https://github.com/DanielOgorchock/linux/pull/35).

Once I saw there were more changes I wanted to make, I decided to share them as a separate out-of-tree kernel driver instead.

Along with Sega Genesis gamepad support, I've also added support for the Nintendo 64 controller for Nintendo Switch Online.

I've since renamed the driver to `hid-nx` to avoid confusion with the in-kernel module. I am in the process of refactoring and reformatting the source code to make it easier to understand and maintain.

### Fork by [mlucianoeze](https://github.com/mlucianoeze)

I've forked the original repository, renaming it from `hid-nx-dkms` to just `hid-nx` so it's not just limited to DKMS.

I then created the needed spec files and built the packages. It took some trial and error but it ended up working just fine, so now there's akmods support in addition to DKMS.


License
-------

    HID driver for Nintendo Switch Joy-Cons and Pro Controllers

    Copyright (c) 2019-2021 Daniel J. Ogorchock <djogorchock@gmail.com>
    Portions Copyright (c) 2020 Nadia Holmquist Pedersen <nadia@nhp.sh>
    Copyright (c) 2022 Emily Strickland <linux@emily.st>

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
    02110-1301, USA.
