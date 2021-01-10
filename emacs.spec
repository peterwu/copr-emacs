# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
%global        _hardened_build 1
%global        debug_package %{nil}
%define        _debugsource_template %{nil}

%global        git_revision a583c72305530f7d3ecc9ba50eefa70b6ddecdd9
%global        git_revision_short %(echo %{git_revision} | head -c 7)
%global        build_timestamp %(date +"%Y%m%d")

Summary:       GNU Emacs text editor
Name:          emacs
Epoch:         1
Version:       28.0.50
Release:       %{build_timestamp}~%{git_revision_short}%{?dist}
License:       GPLv3+ and CC0-1.0
URL:           http://www.gnu.org/software/emacs/
Source0:       https://github.com/emacs-mirror/emacs/archive/%{git_revision}.tar.gz
Source1:       emacs.service

BuildRequires: gcc
BuildRequires: atk-devel
BuildRequires: cairo-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: dbus-devel
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo
BuildRequires: libtiff-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libXpm-devel
BuildRequires: ncurses-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: librsvg2-devel
BuildRequires: m17n-lib-devel
BuildRequires: libotf-devel
BuildRequires: libselinux-devel
BuildRequires: alsa-lib-devel
BuildRequires: gpm-devel
BuildRequires: liblockfile-devel
BuildRequires: libxml2-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: texinfo
BuildRequires: gzip
BuildRequires: desktop-file-utils
BuildRequires: libacl-devel
BuildRequires: harfbuzz-devel
BuildRequires: jansson-devel
BuildRequires: systemd-devel

BuildRequires: gtk3-devel
BuildRequires: webkit2gtk3-devel

BuildRequires: gnupg2

# For docs
BuildRequires: texinfo-tex
BuildRequires: texlive-eurosym

%ifarch %{ix86}
BuildRequires: util-linux
%endif


# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:      desktop-file-utils
Requires:      dejavu-sans-mono-fonts
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Provides:      emacs(bin) = %{epoch}:%{version}-%{release}

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define bytecompargs -batch --no-init-file --no-site-file -f batch-byte-compile
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with support for X windows.

%package nox
Summary:       GNU Emacs text editor without X support
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Provides:      emacs(bin) = %{epoch}:%{version}-%{release}

%description nox
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with no X windows support for running
on a terminal.

%package common
Summary:       Emacs common files
# The entire source code is GPLv3+ except lib-src/etags.c which is
# also BSD.  Manual (info) is GFDL.
License:       GPLv3+ and GFDL and BSD
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      %{name}-filesystem = %{epoch}:%{version}-%{release}
Provides:      %{name}-el = %{epoch}:%{version}-%{release}
Obsoletes:     emacs-el < 1:24.3-29

%description common
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package contains all the common files needed by emacs, emacs-lucid
or emacs-nox.

%package filesystem
Summary:       Emacs filesystem layout
BuildArch:     noarch

%description filesystem
This package provides some directories which are required by other
packages that add functionality to Emacs.

%package devel
Summary: Development header files for Emacs

%description devel
Development header files for Emacs.

%prep
%setup -q -n emacs-%{git_revision}
./autogen.sh

# Sorted list of info files
%define info_files ada-mode auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq-w32 efaq eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido info mairix-el message mh-e newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp url vhdl-mode vip viper widget wisent woman

# Since we are building from the git repo we must also build the info files.
make docs

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

# Avoid duplicating doc files in the common subpackage
%__ln_s ../../%{name}/%{version}/etc/COPYING doc
%__ln_s ../../%{name}/%{version}/etc/NEWS doc


%build
export CFLAGS="-DMAIL_USE_LOCKF %{build_cflags}"
%set_build_flags

# Build GTK+ binary
%__mkdir build-gtk && cd build-gtk
%__ln_s ../configure .

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg --without-xaw3d \
           --with-tiff --without-xft --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json \
           --without-dbus --without-gconf --without-gsettings --without-toolkit-scroll-bars \
           --disable-largefile --without-xim --without-sound --enable-link-time-optimization

%__make bootstrap
%{setarch} %make_build
cd ..

# Build binary without X support
%__mkdir build-nox && cd build-nox
%__ln_s ../configure .
%configure --with-x=no --with-modules --with-json --with-x-toolkit=no --without-xft \
           --without-lcms2 --without-rsvg --disable-largefile --enable-link-time-optimization
%{setarch} %make_build
cd ..

# Remove versioned file so that we end up with .1 suffix and only one DOC file
%__rm build-{gtk,nox}/src/emacs-%{version}.*

# Create pkgconfig file
%__cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{epoch}:%{version}
EOF

# Create macros.emacs RPM macro file
%__cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{?epoch:%{epoch}:}%{version}
%%_emacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
EOF

%install
cd build-gtk
%make_install
cd ..

# Let alternatives manage the symlink
%__rm %{buildroot}%{_bindir}/emacs
touch %{buildroot}%{_bindir}/emacs

# Remove emacs.pdmp from common
%__rm %{buildroot}%{emacs_libexecdir}/emacs.pdmp

# Do not compress the files which implement compression itself (#484830)
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-compr.el.gz
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-cmpr-hook.el.gz

# Install emacs.pdmp of the emacs with GTK+
%__install -p -m 0644 build-gtk/src/emacs.pdmp %{buildroot}%{_bindir}/emacs-%{version}.pdmp

# Install the emacs without X
%__install -p -m 0755 build-nox/src/emacs %{buildroot}%{_bindir}/emacs-%{version}-nox
%__install -p -m 0644 build-nox/src/emacs.pdmp %{buildroot}%{_bindir}/emacs-%{version}-nox.pdmp

# Make sure movemail isn't setgid
%__chmod 755 %{buildroot}%{emacs_libexecdir}/movemail

# This solves bz#474958, "update-directory-autoloads" now finally
# works the path is different each version, so we'll generate it here
echo "(setq source-directory \"%{_datadir}/emacs/%{version}/\")" \
 >> %{buildroot}%{site_lisp}/site-start.el

%__mv %{buildroot}%{_bindir}/{etags,etags.emacs}
%__mv %{buildroot}%{_mandir}/man1/{ctags.1.gz,gctags.1.gz}
%__mv %{buildroot}%{_mandir}/man1/{etags.1.gz,etags.emacs.1.gz}
%__mv %{buildroot}%{_bindir}/{ctags,gctags}
# BZ 927996
%__mv %{buildroot}%{_infodir}/{info.info.gz,info.gz}

%__mkdir -p %{buildroot}%{site_lisp}/site-start.d

# Install pkgconfig file
%__mkdir -p %{buildroot}/%{pkgconfig}
%__install -p -m 0644 emacs.pc %{buildroot}/%{pkgconfig}

# Install rpm macro definition file
%__mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
%__install -p -m 0644 macros.emacs %{buildroot}%{_rpmconfigdir}/macros.d/

# After everything is installed, remove info dir
%__rm -f %{buildroot}%{_infodir}/dir

# Installing service file
%__mkdir -p %{buildroot}%{_userunitdir}
%__install -p -m 0644 %SOURCE1 %{buildroot}%{_userunitdir}/emacs.service
%__rm -f %{buildroot}%{_libdir}/systemd/user/emacs.service

%__rm %{buildroot}%{_datadir}/applications/emacsclient.desktop

#
# Create file lists
#
%__rm -f *-filelist {common,el}-*-files

( TOPDIR=${PWD}
  cd %{buildroot}

  find .%{_datadir}/emacs/%{version}/lisp \
    .%{_datadir}/emacs/%{version}/lisp/leim \
    .%{_datadir}/emacs/site-lisp \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)

)

# Put the lists together after filtering  ./usr to /usr
%__sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
%__cat common-*-files > common-filelist
%__cat el-*-files common-lisp-dir-files > el-filelist

# Remove old icon
%__rm %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document23.svg

%preun
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}

%posttrans
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version} 80

%preun nox
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}-nox
%{_sbindir}/alternatives --remove emacs-nox %{_bindir}/emacs-%{version}-nox

%posttrans nox
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version}-nox 70
%{_sbindir}/alternatives --install %{_bindir}/emacs-nox emacs-nox %{_bindir}/emacs-%{version}-nox 60

%preun common
%{_sbindir}/alternatives --remove emacs.etags %{_bindir}/etags.emacs

%posttrans common
%{_sbindir}/alternatives --install %{_bindir}/etags emacs.etags %{_bindir}/etags.emacs 80 \
       --slave %{_mandir}/man1/etags.1.gz emacs.etags.man %{_mandir}/man1/etags.emacs.1.gz

%files
%{_bindir}/emacs-%{version}
%{_bindir}/emacs-%{version}.pdmp
%attr(0755,-,-) %ghost %{_bindir}/emacs
%{_datadir}/applications/emacs.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/emacs.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/apps/emacs.ico
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg

%files nox
%{_bindir}/emacs-%{version}-nox
%{_bindir}/emacs-%{version}-nox.pdmp
%attr(0755,-,-) %ghost %{_bindir}/emacs
%attr(0755,-,-) %ghost %{_bindir}/emacs-nox

%files common -f common-filelist -f el-filelist
%{_rpmconfigdir}/macros.d/macros.emacs
%license etc/COPYING
%doc doc/NEWS BUGS README
%{_bindir}/ebrowse
%{_bindir}/emacsclient
%{_bindir}/etags.emacs
%{_bindir}/gctags
%{_mandir}/*/*
%{_infodir}/*
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
%{_datadir}/emacs/%{version}/site-lisp
%{_libexecdir}/emacs
%{_userunitdir}/emacs.service
%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/site-start.el
%{pkgconfig}/emacs.pc

%files filesystem
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d

%files devel
%{_includedir}/emacs-module.h

%changelog
* Sun Jan 10 15:45:42 EST 2021 Peter Wu
- git commit a583c72305530f7d3ecc9ba50eefa70b6ddecdd9
* Sun Jan  3 10:58:13 EST 2021 Peter Wu
- add -devel package
- git commit 825b4ec338e82869dc656c7041ab2483b6c22479
* Mon Dec 28 10:42:32 EST 2020 Peter Wu
- adjust build switches to turn off unused features
- git commit 5e1416fd0a41c4b7d13d3cd6ecedab48ae7b55b5
* Fri Dec 25 08:19:00 PM EST 2020 Peter Wu
- use an emacs.service that has ExecStop
- git commit 90e40099debaa876273ae560ed8e66985719dd0c
* Thu Dec 24 09:10:13 PM EST 2020 Peter Wu
- git commit d63ccde966a561756675b9c84b39c724662c82a8
* Fri Dec 18 02:08:58 PM EST 2020 Peter Wu
- roll back native comp support
- git commit e417e87f7ac5b19e84d6767af35e7dec65e77492
* Thu Dec 17 05:58:05 PM EST 2020 Peter Wu
- native comp support
- git commit 87f6e937995c433825173fb0473a801791d5beac
* Thu Dec 17 05:13:55 PM EST 2020 Peter Wu
- added more config switches to the nox build, with credits to AUR:emacs-git
- git commit ddff5d3d879d23f0684b8abe7d923fce4f86ec2e
* Thu Dec 10 2020 Peter Wu
- inherited from emacs.spec from Fedora build
- git commit 8ace7700b93c6c0835ddac6633a7ec07daf56225
* Fri Dec  4 18:48:53 EST 2020 Peter Wu <peterwu@hotmail.com>
- enable LTO
- git commit 39915c708435cefd1c3eaddeec54d3b365d36515
* Wed Dec  2 11:41:51 EST 2020 Peter Wu <peterwu@hotmail.com>
- git commit eff6f0c7f123a79d376f5b06c3a946efb797bb03
