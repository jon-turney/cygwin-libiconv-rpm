%{?cygwin_package_header}

Name:      cygwin-libiconv
Version:   1.16
Release:   2%{?dist}
Summary:   GNU libraries and utilities for character set conversion

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/libiconv/
BuildArch: noarch

Source0:   https://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
Patch0:    libiconv-1.16-wchar.patch
Patch1:    libiconv-1.16-aliases.patch

BuildRequires: cygwin32-filesystem
BuildRequires: cygwin32-gcc
BuildRequires: cygwin32-binutils
BuildRequires: cygwin32

BuildRequires: cygwin64-filesystem
BuildRequires: cygwin64-gcc
BuildRequires: cygwin64-binutils
BuildRequires: cygwin64

BuildRequires: cygwin-aarch64-filesystem
BuildRequires: cygwin-aarch64-gcc
BuildRequires: cygwin-aarch64-binutils
BuildRequires: cygwin-aarch64

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cygwin-libtool-base
BuildRequires: gettext-devel
BuildRequires: make

# There's a quasi-circular dependency between cygwin-libiconv and
# cygwin-gettext.  If gettext is installed when you build this then
# iconv will create *.mo files.  When this package is added to Fedora
# we can consider adding this circular dep:
#BuildRequires: cygwin-gettext


%description
Cygwin Iconv library

%package -n cygwin32-libiconv
Summary:        Cygwin i686 Iconv library
Group:          Development/Libraries

%description -n cygwin32-libiconv
Iconv library for Cygwin i686 toolchain.

%package -n cygwin32-libiconv-static
Summary:        Static version of the i686 Cygwin Iconv library
Group:          Development/Libraries
Requires:       cygwin32-libiconv = %{version}-%{release}

%description -n cygwin32-libiconv-static
Static version of Iconv library for Cygwin i686 toolchain.

%package -n cygwin64-libiconv
Summary:        Cygwin x86_64 Iconv library
Group:          Development/Libraries

%description -n cygwin64-libiconv
Iconv library for Cygwin x86_64 toolchain.

%package -n cygwin64-libiconv-static
Summary:        Static version of the x86_64 Cygwin Iconv library
Group:          Development/Libraries
Requires:       cygwin64-libiconv = %{version}-%{release}

%description -n cygwin64-libiconv-static
Static version of Iconv library for Cygwin x86_64 toolchain.

%package -n cygwin-aarch64-libiconv
Summary:        Cygwin aarch64 Iconv library
Group:          Development/Libraries

%description -n cygwin-aarch64-libiconv
Iconv library for Cygwin aarch64 toolchain.

%package -n cygwin-aarch64-libiconv-static
Summary:        Static version of the aarch64 Cygwin Iconv library
Group:          Development/Libraries
Requires:       cygwin-aarch64-libiconv = %{version}-%{release}

%description -n cygwin-aarch64-libiconv-static
Static version of Iconv library for Cygwin aarch64 toolchain.

%{?cygwin_debug_package}


%prep
%autosetup -p1 -n libiconv-%{version}
rm -f m4/{libtool,lt*}.m4 libcharset/m4/{libtool,lt*}.m4
%cygwin_autoreconf -I `pwd`/m4 -I `pwd`/srcm4 -I `pwd`/libcharset/m4


%build
%global cygwin32_cflags %{cygwin32_cflags} -std=gnu17
%global cygwin64_cflags %{cygwin64_cflags} -std=gnu17
%global cygwin_aarch64_cflags %{cygwin_aarch64_cflags} -std=gnu17

%cygwin_configure \
  --enable-static --enable-shared \
  am_cv_proto_iconv_arg1= \
  am_cv_proto_iconv="extern size_t iconv (iconv_t cd, char * *inbuf, size_t *inbytesleft, char * *outbuf, size_t *outbytesleft);"
%cygwin_make


%install
%cygwin_make_install

# Remove documentation which duplicates what is already in
# Fedora native packages.
rm -rf $RPM_BUILD_ROOT%{cygwin32_docdir}
rm -rf $RPM_BUILD_ROOT%{cygwin32_mandir}
rm -rf $RPM_BUILD_ROOT%{cygwin64_docdir}
rm -rf $RPM_BUILD_ROOT%{cygwin64_mandir}
rm -rf $RPM_BUILD_ROOT%{cygwin_aarch64_docdir}
rm -rf $RPM_BUILD_ROOT%{cygwin_aarch64_mandir}

# If cygwin-gettext was installed during the build, remove the *.mo
# files.  If cygwin-gettext wasn't installed then there won't be any.
rm -rf $RPM_BUILD_ROOT%{cygwin32_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{cygwin64_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{cygwin_aarch64_datadir}/locale

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove unnecessary Cygwin native binaries
rm -f $RPM_BUILD_ROOT%{cygwin32_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{cygwin32_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{cygwin64_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{cygwin64_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{cygwin_aarch64_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{cygwin_aarch64_libdir}/charset.alias


%files -n cygwin32-libiconv
%doc COPYING COPYING.LIB
%{cygwin32_bindir}/cygcharset-1.dll
%{cygwin32_bindir}/cygiconv-2.dll
%{cygwin32_includedir}/iconv.h
%{cygwin32_includedir}/libcharset.h
%{cygwin32_includedir}/localcharset.h
%{cygwin32_libdir}/libcharset.dll.a
%{cygwin32_libdir}/libiconv.dll.a

%files -n cygwin32-libiconv-static
%{cygwin32_libdir}/libcharset.a
%{cygwin32_libdir}/libiconv.a

%files -n cygwin64-libiconv
%doc COPYING COPYING.LIB
%{cygwin64_bindir}/cygcharset-1.dll
%{cygwin64_bindir}/cygiconv-2.dll
%{cygwin64_includedir}/iconv.h
%{cygwin64_includedir}/libcharset.h
%{cygwin64_includedir}/localcharset.h
%{cygwin64_libdir}/libcharset.dll.a
%{cygwin64_libdir}/libiconv.dll.a

%files -n cygwin64-libiconv-static
%{cygwin64_libdir}/libcharset.a
%{cygwin64_libdir}/libiconv.a

%files -n cygwin-aarch64-libiconv
%doc COPYING COPYING.LIB
%{cygwin_aarch64_bindir}/cygcharset-1.dll
%{cygwin_aarch64_bindir}/cygiconv-2.dll
%{cygwin_aarch64_includedir}/iconv.h
%{cygwin_aarch64_includedir}/libcharset.h
%{cygwin_aarch64_includedir}/localcharset.h
%{cygwin_aarch64_libdir}/libcharset.dll.a
%{cygwin_aarch64_libdir}/libiconv.dll.a

%files -n cygwin-aarch64-libiconv-static
%{cygwin_aarch64_libdir}/libcharset.a
%{cygwin_aarch64_libdir}/libiconv.a


%changelog
* Sun Sep 27 2026 Jon Turney <jon.turney@dronecode.org.uk> - 1.16-2
- add aarch64

* Mon Jan 10 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 1.16-1
- new version

* Tue Dec 05 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14-6
- Add aliases patch

* Wed Mar 04 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14-5
- Fix build on EL6

* Fri Jul 25 2014 Yaakov Selkowitz <yselkowitz@cygwin.com> - 1.14-4
- Cleanup spec

* Fri Jun 28 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.14-3
- Rebuild for new Cygwin packaging scheme.
- Add cygwin64 support.

* Mon Oct 31 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.14-2
- Added relocation patch from Cygwin distro.

* Wed Aug 31 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.14-1
- Version bump.

* Wed Feb 16 2011 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 1.13.1-1
- Initial RPM release, largely based on mingw32-iconv.
