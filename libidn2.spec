%define major 0
%define libname %mklibname idn2_ %{major}
%define devname %mklibname idn2 -d

Summary:	Library to support IDNA2008 internationalized domain names
Name:		libidn2
Version:	2.2.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libidn/
Source0:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.lz
Patch0:		libidn2-2.0.0-rpath.patch
BuildRequires:	lzip
BuildRequires:	gettext-devel
BuildRequires:	libunistring-devel
BuildRequires:	texinfo

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
%define oldlibname %mklibname idn2_ 4
%rename %oldlibname
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

%prep
%autosetup -p1

%build
%configure \
	--with-packager="%{vendor}" \
	--with-packager-bug-reports="%{disturl}" \

%make_build

%install
%make_install

# Compatibility with bogus 2.1.0 soname bump
ln -s %{name}.so.0 %{buildroot}%{_libdir}/%{name}.so.4

# Some file cleanups
rm -f %{buildroot}%{_datadir}/info/dir

# Remove example-only binaries for now
rm -f %{buildroot}%{_bindir}/{lookup,register}

%find_lang libidn2

%check
make -C tests check

%files -n idn2
%doc AUTHORS NEWS README.md COPYING COPYING.unicode
%{_bindir}/idn2
%{_mandir}/man1/idn2.1*
%{_infodir}/%{name}.info*

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*
%{_libdir}/%{name}.so.4

%files -n %{devname}
%doc doc/%{name}.html
%doc %{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h
%{_mandir}/man3/*

%files i18n -f %{name}.lang
