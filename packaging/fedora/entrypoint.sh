#!/bin/sh

# Initialize rpmbuild tree
rpmdev-setuptree

# Create tmp directories for tar
mkdir -p /tmp/build
cd /tmp/build

# Create source tarball
version=$(grep -i '^version:' /github/workspace/hid-nx-kmod.spec | awk '{printf "%s", $2}')
mkdir hid-nx-${version}
cp /github/workspace/*.c hid-nx-${version}
cp /github/workspace/*.h hid-nx-${version}
cp /github/workspace/Makefile hid-nx-${version}
tar -czvf hid-nx-${version}.tar.gz hid-nx-${version}
cp hid-nx-${version}.tar.gz ~/rpmbuild/SOURCES/

# Copy spec files where kmodtool expects them
cp /github/workspace/hid-nx-kmod.spec ~/rpmbuild/SPECS/
cp /github/workspace/hid-nx-kmod-common.spec ~/rpmbuild/SPECS/

# Build RPM packages
rpmbuild -ba ~/rpmbuild/SPECS/hid-nx-kmod.spec
rpmbuild -ba ~/rpmbuild/SPECS/hid-nx-kmod-common.spec

# Copy RPM packages to workspace
cd /github/workspace
arch=$(rpm --eval '%{_arch}')
cp ~/rpmbuild/RPMS/${arch}/akmod-hid-nx*.rpm ./
cp ~/rpmbuild/RPMS/${arch}/hid-nx-kmod-common*.rpm ./
