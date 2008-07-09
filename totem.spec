%define build_gstreamer 1
%define build_xine 1
%{?_with_gstreamer: %{expand: %%global build_gstreamer 1}}
%{?_without_gstreamer: %{expand: %%global build_gstreamer 0}}
%{?_with_xine: %{expand: %%global build_xine 1}}
%{?_without_xine: %{expand: %%global build_xine 0}}
%define build_mozilla 1

%define xineversion 1.1.2
%define gstver 0.10

%define major 0
%define soname %{major}.0.0
%define libnamexine %mklibname baconvideowidget-xine %major
%define libnamegstreamer %mklibname baconvideowidget-gstreamer %major

%define backend_suffix %{nil}
%if %_lib != lib
%define backend_suffix -64
%endif

Summary: Movie player for GNOME 2
Name: totem
Version: 2.23.4
Release: %mkrel 2
Source0: http://ftp.gnome.org/pub/GNOME/sources/totem/%{name}-%{version}.tar.bz2
Source1: %name-48.png
#gw from Fedora:
# http://cvs.fedoraproject.org/viewcvs/rpms/totem/devel/totem-bin-backend-ondemand.sh
Source2: totem-bin-backend-ondemand.sh
Patch: totem-r5484-vala-includes.patch
Patch1: totem-2.23.4-fix-linking.patch
License: GPLv2 with exception
Group: Video
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://www.hadess.net/totem.php3
%if %build_gstreamer
BuildRequires: libgstreamer-plugins-base-devel >= %gstver
BuildRequires: gstreamer0.10-plugins-good
BuildRequires: gstreamer0.10-plugins-base
%endif
%if %build_xine
BuildRequires: libxine-devel >= %xineversion
%endif
BuildRequires: libxdmcp-devel
BuildRequires: libxtst-devel
BuildRequires: libxxf86vm-devel
BuildRequires: libnvtvsimple-devel
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils
BuildRequires: liblirc-devel
BuildRequires: libnautilus-devel
BuildRequires: libgalago-devel
BuildRequires: libvala-devel >= 0.1.5
BuildRequires: libbluez-devel
BuildRequires: libepc-devel
BuildRequires: hal-devel
BuildRequires: glib2-devel >= 2.9.6
BuildRequires: iso-codes
BuildRequires: intltool
BuildRequires: automake1.9
BuildRequires: gnome-common
BuildRequires: desktop-file-utils
BuildRequires: shared-mime-info >= 0.22
BuildRequires: libgnome-window-settings-devel
BuildRequires: pygtk2.0-devel
BuildRequires: gtk2-devel >= 2.12.1
BuildRequires: libtotem-plparser-devel >= 2.21.90


%description
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.
This version is based on the xine backend.


%package common
Summary: Common data files for totem 
Group:	Video
Requires: pygtk2.0
Requires: iso-codes
Requires: python-gdata
Requires(post)  : scrollkeeper >= 0.3 desktop-file-utils
Requires(postun): scrollkeeper >= 0.3 desktop-file-utils

%description common
Common data files used by Totem.

%if %build_xine
%package xine
Summary: %{summary}
Group:	Video
Requires: %libnamexine = %version-%release
Requires: %name-common = %version
Provides:  totem
Obsoletes: totem < 2.23

%description xine
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

This version is based on the xine backend.
%endif

%if %build_gstreamer
%package gstreamer
Summary: %{summary}
Group:	Video
Requires: %libnamegstreamer = %{version}-%{release}
Requires: %name-common = %version
Provides: totem

%description gstreamer
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

This version is based on the gstreamer backend.
%endif


%if %build_mozilla
%package mozilla
Summary: Totem video plugin for Mozilla Firefox
Group: Networking/WWW
BuildRequires: mozilla-firefox-devel
BuildRequires: dbus-devel >= 0.35
%define firefox_version %(rpm -q mozilla-firefox --queryformat %{VERSION})
Requires: %mklibname mozilla-firefox %{firefox_version}
Requires: totem-common = %version
Obsoletes: totem-mozilla-gstreamer
Provides: totem-mozilla-gstreamer

%description mozilla
This embeds the Totem video player into web browsers based on Mozilla Firefox.
This version is based on the xine backend.
%endif

%package nautilus
Group:Video
Summary: Video and Audio Properties tab for Nautilus
Requires: %name-common = %version

%description nautilus
A Nautilus extension that shows the properties of audio and video
files in the properties dialogue.


%package -n %libnamexine
Summary: Totem video widget shared library, xine backend
Group: System/Libraries
Requires: xine-plugins >= %xineversion

%description -n %libnamexine
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

This is the Widget library based on xine shared among the totem
components.

%if %build_gstreamer
%package -n %libnamegstreamer
Summary: Totem video widget shared library, xine backend
Group: System/Libraries
Requires: gstreamer0.10-plugins-base >= %gstver
Requires: gstreamer0.10-plugins-good

%description -n %libnamegstreamer
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

This is the Widget library based on xine shared among the totem
components.
%endif

%prep
%setup -q
%patch -p1
%patch1 -p1
libtoolize --copy --force
aclocal
autoconf
automake
%build
#gw else libthumbnail.la does not build
%define _disable_ld_no_undefined 1
%if %build_xine
# Build xine version
[ -d xine-build ] || mkdir xine-build
cd xine-build

CONFIGURE_TOP=.. %configure2_5x --disable-run-in-source-tree \
%if %build_mozilla
--enable-browser-plugins \
%else
--disable-browser-plugins \
%endif
--enable-xine
%make
cd ..
%endif

%if %build_gstreamer
# Build gstreamer version
[ -d gstreamer-build ] || mkdir gstreamer-build
cd gstreamer-build

CONFIGURE_TOP=.. %configure2_5x --disable-run-in-source-tree \
%if %build_mozilla
--enable-browser-plugins \
%else
--disable-browser-plugins \
%endif


%make
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%if %build_xine
pushd xine-build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
mv %buildroot%_libdir/libbaconvideowidget.so.%{soname} %buildroot%_libdir/libbaconvideowidget-xine.so.%{soname}
popd

cat > %buildroot%_bindir/totem-xine << EOF
#!/bin/sh
%_bindir/totem-backend -b xine totem "\$@"
EOF
%endif

%if %build_gstreamer
pushd gstreamer-build/
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
mv %buildroot%_libdir/libbaconvideowidget.so.%{soname} %buildroot%_libdir/libbaconvideowidget-gstreamer.so.%{soname}
popd

cat > %buildroot%_bindir/totem-gstreamer << EOF
#!/bin/sh
%_bindir/totem-backend -b gstreamer totem "\$@"
EOF
%endif

install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}-backend

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

#menu
MIME_TYPES=`tr '\n' , < data/mime-type-list.txt | sed -e 's/,$//'`
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p %buildroot{%_liconsdir,%_miconsdir,%_iconsdir}
mkdir -p %buildroot%_iconsdir/hicolor/48x48/apps
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%name.png
install -D -m 644 data/icons/16x16/totem.png $RPM_BUILD_ROOT%{_miconsdir}/%name.png
install -D -m 644 data/icons/32x32/totem.png $RPM_BUILD_ROOT%{_iconsdir}/%name.png
install -D -m 644 %{SOURCE1} %buildroot/%_liconsdir/%name.png


# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/{totem/plugins/*/,mozilla/plugins,nautilus/extensions-2.0}/*.{la,a} %buildroot/var/lib/scrollkeeper


#gw there is no devel package yet
rm -f %buildroot%_libdir/libbaconvideowidget.{a,la,so}



%clean
rm -rf $RPM_BUILD_ROOT

%post common
%define schemas totem totem-video-thumbnail totem-handlers
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%update_desktop_database
%update_menus
%update_scrollkeeper
%endif
update-alternatives --remove totem %_bindir/totem-xine
update-alternatives --remove totem %_bindir/totem-gstreamer
update-alternatives --remove totem-mozilla %_libexecdir/totem-plugin-viewer-xine
update-alternatives --remove totem-mozilla %_libexecdir/totem-plugin-viewer-gstreamer

%preun common
%preun_uninstall_gconf_schemas %schemas

%postun common
%if %mdkversion < 200900
%clean_scrollkeeper
%clean_icon_cache hicolor
%clean_desktop_database
%clean_menus
%endif

%if %build_xine
%post -n %libnamexine
/usr/sbin/alternatives --install %{_libdir}/libbaconvideowidget.so.%{soname} totem-backend%{backend_suffix} %{_libdir}/libbaconvideowidget-xine.so.%{soname} 20
/sbin/ldconfig
%postun -n %libnamexine
[ -e "%{_libdir}/libbaconvideowidget-xine.so.%{soname}" ] || update-alternatives --remove totem-backend%{backend_suffix} %{_libdir}/libbaconvideowidget-xine.so.%{soname}
%endif

%if %build_gstreamer
%post -n %libnamegstreamer
/usr/sbin/alternatives --install %{_libdir}/libbaconvideowidget.so.%{soname} totem-backend%{backend_suffix} %{_libdir}/libbaconvideowidget-gstreamer.so.%{soname} 10
/sbin/ldconfig
%postun -n %libnamegstreamer
[ -e "%{_libdir}/libbaconvideowidget-gstreamer.so.%{soname}" ] || update-alternatives --remove totem-backend%{backend_suffix} %{_libdir}/libbaconvideowidget-gstreamer.so.%{soname}
%endif

%files common -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS TODO NEWS data/lirc_example
%_sysconfdir/gconf/schemas/totem.schemas
%_sysconfdir/gconf/schemas/totem-handlers.schemas
%_sysconfdir/gconf/schemas/totem-video-thumbnail.schemas
%dir %_datadir/omf/totem/
%_datadir/icons/hicolor/*/apps/*
%_datadir/omf/totem/totem-C.omf
%_datadir/totem
%_datadir/applications/totem.desktop
%dir %_libdir/totem
%_libdir/totem/plugins
%_libdir/totem/totem-bugreport.py
%_mandir/man1/*
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_liconsdir}/%name.png
%defattr(-,root,root)
%_bindir/totem
%_bindir/totem-audio-preview
%_bindir/totem-backend
%_bindir/totem-video-indexer
%_bindir/totem-video-thumbnailer


%if %build_xine
%files xine
%attr(755,root,root) %_bindir/totem-xine
%endif


%files nautilus
%defattr(-,root,root)
%_libdir/nautilus/extensions-2.0/*

%if %build_gstreamer
%files gstreamer
%defattr(-,root,root)
%attr(755,root,root) %_bindir/totem-gstreamer
%endif

%if %build_mozilla
%files mozilla
%defattr(-,root,root)
%_libdir/mozilla/plugins/libtotem*.so
%_libexecdir/totem-plugin-viewer
%endif

%if %build_xine
%files -n %libnamexine
%defattr(-,root,root)
%_libdir/libbaconvideowidget-xine.so.%{soname}
%ghost %_libdir/libbaconvideowidget.so.%{major}
%endif

%if %build_gstreamer
%files -n %libnamegstreamer
%defattr(-,root,root)
%_libdir/libbaconvideowidget-gstreamer.so.%{soname}
%ghost %_libdir/libbaconvideowidget.so.%{major}
%endif
