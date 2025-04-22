%define keepstatic 1
%global freetype_version 2.1.4

Name:       fontconfig
Summary:    Font configuration and customization library
Version:    2.13.96
Release:    1
License:    MIT
URL:        https://github.com/sailfishos/fontconfig
Source0:    fontconfig-%{version}.tar.gz
Source1:    10-antialias.conf
Source2:    10-hinted.conf
Source3:    25-no-bitmap-fedora.conf
Requires:   fontpackages-filesystem
Requires(post): freetype >= %{freetype_version}
Requires(post): coreutils
Requires(post): /usr/bin/grep
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  expat-devel
BuildRequires:  gperf
BuildRequires:  gettext
BuildRequires:  python3-base

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.


%package devel
Summary:    Font configuration and customization library
Requires:   %{name} = %{version}-%{release}
Requires:   freetype-devel >= %{freetype_version}

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%package devel-static
Summary:    Font configuration and customization library
#Requires:   %{name} = %{version}-%{release}
#Requires:   freetype-devel >= %{freetype_version}

%description devel-static
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.



%prep
%autosetup -p1 -n %{name}-%{version}/%{name}


%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

NOCONFIGURE=1 sh autogen.sh
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure --enable-static
%make_build

%install
rm -rf %{buildroot}

%make_install

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/fontconfig/conf.avail
ln -s %{_datadir}/fontconfig/conf.avail/10-autohint.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/10-antialias.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/10-hinted.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_datadir}/fontconfig/conf.avail/25-no-bitmap-fedora.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
rm -rf $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES/fontconfig.mo

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts


%post
/sbin/ldconfig
umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig
# Remove stale caches
rm -f %{_localstatedir}/cache/fontconfig/????????????????????????????????.cache-2
rm -f %{_localstatedir}/cache/fontconfig/stamp

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-pattern
%{_bindir}/fc-validate
%{_bindir}/fc-conflist
%dir %{_datadir}/fontconfig/conf.avail
%dir %{_datadir}/fonts
%{_datadir}/xml/fontconfig/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf
%{_datadir}/fontconfig/conf.avail/*.conf
%config %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig


%files devel
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig
%doc %{_sysconfdir}/fonts/conf.d/README
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc
%{_datadir}/locale/zh_CN/LC_MESSAGES/fontconfig-conf.mo

%files devel-static
%defattr(-, root, root)
%{_libdir}/*.a
