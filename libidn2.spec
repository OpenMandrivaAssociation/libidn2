# libidn2 is used by systemd, libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global build_ldflags %{build_ldflags} -Wl,--undefined-version

%if %{cross_compiling}
# FIXME help2man by nature doesn't work while crosscompiling,
# but just replacing it with "true" isn't good...
%define hm HELP2MAN=true
%else
%define hm %{nil}
%endif

# static libraries are needed by qemu

%define major 0
%define oldlibname %mklibname idn2_ 0
%define libname %mklibname idn2
%define devname %mklibname idn2 -d
%define sdevname %mklibname idn2 -d -s

%define lib32name libidn2_%{major}
%define dev32name libidn2-devel
%define sdev32name libidn2-static-devel

%global optflags %{optflags} -O3

Summary:	Library to support IDNA2008 internationalized domain names
Name:		libidn2
Version:	2.3.4
Release:	5
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.gnu.org/software/libidn/
Source0:	https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Patch0:		libidn2-2.0.0-rpath.patch
Patch1:		libidn-2.3.3-clang.patch
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libunistring)
BuildRequires:	texinfo
BuildRequires:	gtk-doc
%if %{with compat32}
BuildRequires:	devel(libunistring)
BuildRequires:	libc6
%endif

%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package -n %{libname}
Summary:	Internationalized string processing library %{name}
Group:		System/Libraries
Requires:	%{name}-i18n >= %{EVRD}
# 2.1.0 bumped the soname to 4, 2.1.1 realized there wasn't
# actually an ABI change and went back to 0...
%define olderlibname %mklibname idn2_ 4
%rename %oldlibname
%rename %olderlibname
%if "%_lib" == "lib"
Provides:	libidn2.so.4
Provides:	libidn2.so.4(IDN2_0.0.0)
%else
Provides:	libidn2.so.4()(64bit)
Provides:	libidn2.so.4(IDN2_0.0.0)(64bit)
%endif

%description -n %{libname}
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package -n %{devname}
Summary:	Development files for the %{name} library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Provides:	idn2-devel = %{EVRD}
Requires:	%{libname} >= %{EVRD}

%description -n %{devname}
Development files for the %{name} library.

%package -n %{sdevname}
Summary:	Static libraries for the %{name} library
Group:		Development/C
Provides:	idn2-static-devel = %{EVRD}
Requires:	%{devname} >= %{EVRD}

%description -n %{sdevname}
Static libraries for the %{name} library.

%package -n idn2
Summary:	Command line interface to the Libidn2 implementation of IDNA2008
Group:		System/Servers

%description -n idn2
Internationalized Domain Name (IDNA2008) convert STRINGS, or standard input.

%package i18n
Summary:	Internationalization and locale data for %{name}
Group:		System/Internationalization
BuildArch:	noarch

%description i18n
Internationalization and locale data for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Internationalized string processing library %{name} (32-bit)
Group:		System/Libraries
Requires:	%{name}-i18n >= %{EVRD}

%description -n %{lib32name}
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package -n %{dev32name}
Summary:	Development files for the %{name} library
Group:		Development/C
Requires:	%{devname} >= %{EVRD}
Requires:	%{lib32name} >= %{EVRD}

%description -n %{dev32name}
Development files for the %{name} library.

%package -n %{sdev32name}
Summary:	Static libraries for the %{name} library
Group:		Development/C
Requires:	%{dev32name} >= %{EVRD}

%description -n %{sdev32name}
Static libraries for the %{name} library.
%endif

%prep
%autosetup -p1
autoreconf -fiv

%build
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-static \
	--with-packager="%{vendor}" \
	--with-packager-bug-reports="%{disturl}"
cd ..
%endif

mkdir build
cd build
%configure \
	--with-packager="%{vendor}" \
	--with-packager-bug-reports="%{disturl}" \
	--enable-static \
	--enable-gtk-doc
cd ..

%if %{with compat32}
%make_build -C build32 %{hm}
%endif
%make_build -C build %{hm}

%install
%if %{with compat32}
%make_install -C build32 %{hm}
%endif
%make_install -C build %{hm}

# Compatibility with bogus 2.1.0 soname bump
ln -s %{name}.so.0 %{buildroot}%{_libdir}/%{name}.so.4

# Some file cleanups
rm -f %{buildroot}%{_datadir}/info/dir

# Remove example-only binaries for now
rm -f %{buildroot}%{_bindir}/{lookup,register}

%find_lang libidn2

# As of 2.3.3, the testsuite is broken (fails to build)
# Please re-enable when fixed.
%if 0
%check
%if %{with compat32}
make -C build32/tests check
%endif
make -C build/tests check
%endif

%files -n idn2
%doc AUTHORS NEWS README.md COPYING COPYING.unicode
%{_bindir}/idn2
%doc %{_mandir}/man1/idn2.1*
%doc %{_infodir}/%{name}.info*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}.so.4

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h
%doc %{_mandir}/man3/*

%files -n %{sdevname}
%{_libdir}/lib*.a

%files i18n -f %{name}.lang

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/%{name}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/%{name}.so
%{_prefix}/lib/pkgconfig/%{name}.pc

%files -n %{sdev32name}
%{_prefix}/lib/lib*.a
%endif
