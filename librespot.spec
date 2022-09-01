Name:       librespot
Version:    0.4.2
Release:    1%{?dist}
Summary:    An open source client for Spotify, with support for Spotify Connect 

License:    MIT
URL:        https://github.com/librespot-org/librespot/
Source0:    https://github.com/librespot-org/librespot/archive/v%{version}/librespot-%{version}.tar.gz

# Contains librespot-$VERSION/vendor/*.
#     $ cargo vendor
#     $ mkdir librespot-X.Y.Z
#     $ mv vendor librespot-X.Y.Z/
#     $ tar vcJf librespot-X.Y.Z.cargo-vendor.tar.xz librespot-X.Y.Z
Source1:    librespot-%{version}.cargo-vendor.tar.xz
Source2:    config.toml

Source3:    librespot.service

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  avahi-compat-libdns_sd-devel


%description
librespot is an open source client library for Spotify. It enables applications
to use Spotify's service to control and play music via various backends, and to
act as a Spotify Connect receiver. It is an alternative to the official and now
deprecated closed-source libspotify. Additionally, it will provide extra
features which are not available in the official library.


%prep
%autosetup -b1 -n librespot-%{version}

mkdir .cargo
cp %{SOURCE2} .cargo/


%build
export RUSTFLAGS=-g
%{__cargo} build %{?_smp_mflags} -Z avoid-dev-deps --frozen --release \
        --bin "librespot" \
        --no-default-features \
        --features "alsa-backend,pulseaudio-backend,with-dns-sd"


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_userunitdir}

cp target/release/librespot %{buildroot}/%{_bindir}/
cp %{SOURCE3} %{buildroot}/%{_userunitdir}/


%files
%{_bindir}/librespot
%{_userunitdir}/librespot.service
%license LICENSE


%post
%systemd_user_post %{name}.service


%preun
%systemd_user_preun %{name}.service


%changelog
* Thu Sep 01 2022 Ivan Mironov <mironov.ivan@gmail.com> - 0.4.2-1
- Initial packaging
