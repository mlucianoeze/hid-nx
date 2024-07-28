FROM fedora:latest

# Install dependencies
RUN dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
RUN dnf -y install buildsys-build-rpmfusion akmods rpmdevtools

# Initialize RPM tree
RUN rpmdev-setuptree

# Set entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
