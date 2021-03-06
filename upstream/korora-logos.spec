Name:       korora-logos
Version:    23.0
Release:    1%{?dist}
Summary:    Icons and pictures

Group:      System Environment/Base
URL:        http://kororaproject.org
Source0:    %{name}-%{version}.tar.gz
#The KDE Logo is under a LGPL license (no version statement)
License:    GPLv2 and LGPLv2+
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

Obsoletes:  redhat-logos
Obsoletes:  generic-logos < 17.0.0-5
Provides:   redhat-logos = %{version}-%{release}
Provides:   system-logos = %{version}-%{release}

Obsoletes:  fedora-logos kororaa-logos
Provides:   fedora-logos kororaa-logos
Conflicts:  anaconda-images <= 10
Conflicts:  redhat-artwork <= 5.0.5
BuildRequires: hardlink
# For _kde4_* macros:
BuildRequires: kde-filesystem
# For generating the EFI icon
BuildRequires: libicns-utils
Requires(post): coreutils

%description
The korora-logos package contains various image files which can be
used by the bootloader, anaconda, and other related tools.

%package httpd
Summary: Fedora-related icons and pictures used by httpd
Provides: system-logos-httpd = %{version}-%{release}
Provides: fedora-logos-httpd = %{version}-%{release}
Obsoletes: system-logos-httpd
Obsoletes: fedora-logos-httpd
Obsoletes:  generic-logos < 17.0.0-5
BuildArch: noarch

%description httpd
The generic-logos-httpd package contains image files which can be used by
httpd.

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}

# should be ifarch i386
mkdir -p %{buildroot}/boot/grub
install -p -m 644 bootloader/splash.xpm.gz %{buildroot}/boot/grub/splash.xpm.gz
# end i386 bits


mkdir -p %{buildroot}%{_datadir}/firstboot/themes/generic
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/generic                                  
done

mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.vol %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora-media.vol  %{buildroot}%{_datadir}/pixmaps/bootloader

mkdir -p %{buildroot}%{_datadir}/pixmaps/splash
for i in gnome-splash/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps/splash
done

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

mkdir -p %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
mkdir -p %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
install -p -m 644 ksplash/SolarComet-kde.png %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
for i in plymouth/charge/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
done

# File or directory names do not count as trademark infringement
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
install -p -m 644 icons/Fedora/scalable/apps/* %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/

(cd anaconda; make DESTDIR=%{buildroot} install)

# save some dup'd icons
/usr/sbin/hardlink -v %{buildroot}/

%post
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/Fedora-KDE/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/Fedora-KDE/index.theme || :
  fi
fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/oxygen/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/oxygen/index.theme || :
  fi
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING-kde-logo README
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/boot/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/Fedora/*/apps/*
%{_datadir}/pixmaps/*
%exclude %{_datadir}/pixmaps/poweredby.png
%{_datadir}/plymouth/themes/charge/*
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
%{_kde4_iconsdir}/oxygen/
# should be ifarch i386
/boot/grub/splash.xpm.gz
# end i386 bits

%files httpd
%doc COPYING
%{_datadir}/pixmaps/poweredby.png

%changelog
* Sun Oct 18 2015 Chris Smart <csmart@kororaproject.org> - 23.0-1
- Update for Korora 23 release.

* Sun Dec 28 2014 Chris Smart <csmart@kororaproject.org> - 21.0-1
- Update for Korora 21 release.

* Sun Oct 27 2013 Chris Smart <csmart@kororaproject.org> - 20.0-1
- Update for Korora 20 release.

* Sat May 11 2013 Ian Firns <firnsy@kororaproject.org> - 19.0-1
- Update for Korora 19 release.

* Thu Oct 25 2012 Chris Smart <csmart@kororaproject.org> - 18.0.0-1
- Update for Korora 18 release.

* Fri Jul 6 2012 Chris Smart <chris@kororaa.org> - 17.0.0-1
- Update for Kororaa 17 release.

* Thu Nov 10 2011 Chris Smart <chris@kororaa.org> - 16.0.0-1
- Update for Kororaa 16 release.

* Sat Oct 15 2011 Chris Smart <chris@kororaa.org> - 15.0.0-3
- Re-draw some plymouth artwork to fix Firnsy's complaint about it "jumping all over the place" :-)

* Sun Aug 04 2011 Chris Smart <chris@kororaa.org> - 15.0.0-2
- Add Replaces fedora-logos.

* Sun Jul 10 2011 Chris Smart <chris@kororaa.org> - 15.0.0-1
- Updated for Fedora 15.

* Mon Apr 25 2011 Chris Smart <chris@kororaa.org> - 14.0.4-1
- Added Kororaa logo to Anaconda artwork.

* Sat Feb 26 2011 Chris Smart <chris@kororaa.org> - 14.0.1-1
- initial port from Fedora.

