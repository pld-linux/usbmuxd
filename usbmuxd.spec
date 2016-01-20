#
# Conditional build:
%bcond_without	preflight		# preflight worker support

Summary:	Daemon for communicating with Apple's iPod Touch and iPhone
Summary(pl.UTF-8):	Demon do komunikacji z urządzeniami iPod Touch i iPhone firmy Apple
Name:		usbmuxd
Version:	1.0.9
Release:	0.1
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:	GPL v2+ (daemon) and LGPL v2.1+ (library)
Group:		Daemons
#Source0Download: http://www.libimobiledevice.org/
Source0:	http://www.libimobiledevice.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	e98dff7fcf71ac8f218555abb02088e4
Source1:	https://github.com/libimobiledevice/usbmuxd/raw/1.0.9/src/%{name}-proto.h
# Source1-md5:	0cb310cb35a8746d71db5ee160cc385c
URL:		http://www.libimobiledevice.org/
%{?with_preflight:BuildRequires:	libimobiledevice >= 1.1.6}
BuildRequires:	libplist-devel >= 1.11
BuildRequires:	libusb-devel >= 1.0.3
BuildRequires:	rpmbuild(macros) >= 1.600
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(usbmux)
Provides:	user(usbmux)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and
iPhone devices. It allows multiple services on the device to be
accessed simultaneously.

%description -l pl.UTF-8
usbmuxd jest demonem używanym do komunikacji z urządzeniami iPod Touch
i iPhone firmy Apple. Umożliwia jednoczesny dostęp do kilku usług na
urządzeniu.

%package libs
Summary:	libusbmuxd library
Summary(pl.UTF-8):	Biblioteka libusbmuxd
Group:		Libraries
Requires:	libusb >= 1.0.3

%description libs
libusbmuxd is a library to communicate with the usbmux daemon.

%description libs -l pl.UTF-8
libusbmuxd jest biblioteką do komunikacji z demonem usbmux.

%package devel
Summary:	Header files for libusbmuxd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libusbmuxd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libusb-devel >= 1.0.3

%description devel
Header files for libusbmuxd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libusbmuxd.

%prep
%setup -q

# missing from source
cp -p %{SOURCE1} src

%build
%configure \
	--disable-silent-rules \
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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
#%attr(755,root,root) %{_bindir}/iproxy
%attr(755,root,root) %{_sbindir}/usbmuxd
%{_mandir}/man1/usbmuxd.1*
/lib/udev/rules.d/39-usbmuxd.rules
%{systemdunitdir}/usbmuxd.service

%files libs
%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/libusbmuxd.so.*.*.*
#%attr(755,root,root) %ghost %{_libdir}/libusbmuxd.so.2

%files devel
%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/libusbmuxd.so
#%{_includedir}/usbmuxd-proto.h
#%{_includedir}/usbmuxd.h
#%{_pkgconfigdir}/libusbmuxd.pc
