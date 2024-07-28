%global _modprobe_d     %{_prefix}/lib/modprobe.d/

%define module hid-nx

Name: %{module}-kmod-common

Version:        1.14
Release:        1%{?dist}.1
Summary:        Linux kernel HID driver for Nintendo Switch controllers - common files

Group:          System Environment/Kernel

License:        GPL-2.0-or-later
URL:            https://github.com/mlucianoeze/%{module}
Requires:       %{module}-kmod = %{version}
Provides:       %{module}-kmod-common = %{version}

%description
This package provides common files for hid-nx-kmod.

%prep
# No prep

%build
# No build

%install
mkdir -p %{buildroot}%{_modprobe_d}/
echo 'blacklist hid-nintendo' > %{buildroot}%{_modprobe_d}/hid-nx.conf

%files
%{_modprobe_d}/hid-nx.conf

