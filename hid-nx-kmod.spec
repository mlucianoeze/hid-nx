%if 0%{?fedora}
%global buildforkernels akmod
%endif
%global debug_package %{nil}

%define module hid-nx

# name should have a -kmod suffix
Name: %{module}-kmod

Version:        1.14
Release:        1%{?dist}.1
Summary:        Linux kernel HID driver for Nintendo Switch controllers

Group:          System Environment/Kernel

License:        GPL-2.0-or-later
URL:            https://github.com/mlucianoeze/%{module}
Source0:        %{module}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{_bindir}/kmodtool


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
# ExclusiveArch:  i686 x86_64 ppc64 ppc64le armv7hl aarch64
# ExcludeArch: i686 x86_64 ppc64 ppc64le armv7hl aarch64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
This module is an HID driver for the Nintendo Switch controllers.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{module} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
# pushd %{module}-%{version}
# #patch0 -p1 -b .suffix
# popd

for kernel_version in %{?kernel_versions} ; do
    cp -a %{module}-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
rm -rf ${RPM_BUILD_ROOT}

for kernel_version in %{?kernel_versions}; do
    # make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -D -m 755 _kmod_build_${kernel_version%%___*}/%{module}.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{module}.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Jun 30 2024 Luciano Marti <mlucianoeze@gmail.com> - 1.14-1
- Initial package based on version 1.14

