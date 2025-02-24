Summary:        Define and run multi-container applications with Docker
Name:           moby-compose
Version:        2.17.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Tools/Container
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Leverage the `generate_source_tarball.sh` to create the vendor sources
# NOTE: govendor-v1 format is for inplace CVE updates so that we do not have to overwrite in the blob-store.
# After fixing any possible CVE for the vendored source, we must bump v1 -> v2
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang
Requires:       moby-cli


%description
Compose is a tool for defining and running multi-container Docker applications.
With Compose, you use a YAML file to configure your application’s services.
Then, with a single command, you create and start all the services from your
configuration.

%prep
%autosetup -n compose-%{version}
%setup -q -n compose-%{version} -T -D -a 1

%build
go build \
	   -mod=vendor \
	   -trimpath \
	   -tags e2e \
	   -ldflags "-w -X github.com/docker/compose/v2/internal.Version=%{version}" \
	   -o ./bin/build/docker-compose ./cmd

%install
mkdir -p "%{buildroot}/%{_libexecdir}/docker/cli-plugins"
install -D -m0755 bin/build/docker-compose %{buildroot}/%{_libexecdir}/docker/cli-plugins

%files
%license LICENSE
%{_libexecdir}/docker/cli-plugins/docker-compose

%changelog
* Tue Mar 14 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 2.17.2-1
- Original version for CBL-Mariner
- License Verified
