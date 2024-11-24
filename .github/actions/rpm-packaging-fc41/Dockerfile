FROM fedora:41

# Install dependencies
RUN dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
RUN dnf -y install buildsys-build-rpmfusion akmods rpmdevtools

# Set entrypoint
COPY ../../common/rpm-packaging/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
