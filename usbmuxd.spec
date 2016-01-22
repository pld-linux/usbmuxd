# TODO
# - add systemd and udev support both
#   - install appropriate udev rule with udev opts
#   - install appropriate systemd file with systemd opts
#   - make them not to conflict
#   - their "support" itself is just imply other options:
#     -u, --udev    Run in udev operation mode (implies -n and -z)
#     -s, --systemd Run in systemd operation mode (implies -z and -f)
#
# Conditional build:
%bcond_without	preflight		# preflight worker support

Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Summary(pl.UTF-8):	Demon do komunikacji z urządzeniami iPod Touch i iPhone firmy Apple
Name:		usbmuxd
Version:	1.1.0
Release:	1
License:	GPL v2 or GPL v3
Group:		Daemons
#Source0Download: http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	34361c59320cb0b1f9ebcd2798ee1b39
URL:		http://www.libimobiledevice.org/
%{?with_preflight:BuildRequires:	libimobiledevice-devel >= 1.1.6}
BuildRequires:	libplist-devel >= 1.11
BuildRequires:	libusb-devel >= 1.0.3
BuildRequires:	libusbmuxd-devel >= 1.0.9
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	systemd-units
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
%{?with_preflight:Requires:	libimobiledevice >= 1.1.6}
Requires:	libplist >= 1.11
Requires:	libusb >= 1.0.3
Provides:	group(usbmux)
Provides:	user(usbmux)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and
iPhone devices. It allows multiple services on the device to be
accessed simultaneously.

%description -l pl.UTF-8
usbmuxd jest demonem używanym do komunikacji z urządzeniami iPod Touch
i iPhone firmy Apple. Umożliwia jednoczesny dostęp do kilku usług na
urządzeniu.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--without-systemd \
	%{!?with_preflight:--without-preflight}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 247 usbmux
%useradd -u 247 -g usbmux -c "usbmuxd daemon" usbmux

%postun
if [ "$1" = "0" ]; then
	%userremove usbmux
	%groupremove usbmux
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_sbindir}/usbmuxd
%{_mandir}/man1/usbmuxd.1*
/lib/udev/rules.d/39-usbmuxd.rules
