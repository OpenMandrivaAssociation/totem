%define build_mozilla 1

%define gstver 0.10.22.4

%define backend_suffix %{nil}
%if %_lib != lib
%define backend_suffix -64
%endif

Summary: Movie player for GNOME 2
Name: totem
Version: 2.27.1
Release: %mkrel 1
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
Source1: %name-48.png
License: GPLv2 with exception
Group: Video
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://www.hadess.net/totem.php3
BuildRequires: libgstreamer-plugins-base-devel >= %gstver
BuildRequires: gstreamer0.10-plugins-good
BuildRequires: gstreamer0.10-plugins-base
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
BuildRequires: libtotem-plparser-devel >= 2.27.0
BuildRequires: unique-devel
Requires: gnome-python-gconf
Requires: pygtk2.0
Requires: iso-codes
Requires: gstreamer0.10-plugins-base >= %gstver
Requires: gstreamer0.10-plugins-good
#gw opensubtitles plugin:
Requires: pyxdg
Requires(post)  : scrollkeeper >= 0.3 desktop-file-utils
Requires(postun): scrollkeeper >= 0.3 desktop-file-utils
Provides: %name-common %name-gstreamer %name-xine
Obsoletes: %name-common %name-gstreamer %name-xine

%description
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.


%if %build_mozilla
%package mozilla
Summary: Totem video plugin for Mozilla Firefox
Group: Networking/WWW
BuildRequires: dbus-devel >= 0.35
Requires: totem-common = %version
Obsoletes: totem-mozilla-gstreamer
Provides: totem-mozilla-gstreamer

%description mozilla
This embeds the Totem video player into web browsers based on Mozilla Firefox.
%endif

%package nautilus
Group:Video
Summary: Video and Audio Properties tab for Nautilus
Requires: %name-common = %version

%description nautilus
A Nautilus extension that shows the properties of audio and video
files in the properties dialogue.

%prep
%setup -q

%build
#gw else libthumbnail.la does not build
%define _disable_ld_no_undefined 1

%configure2_5x --disable-run-in-source-tree \
%if %build_mozilla
--enable-browser-plugins \
%else
--disable-browser-plugins \
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
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

%post
%define schemas totem totem-video-thumbnail totem-handlers
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%update_desktop_database
%update_menus
%update_scrollkeeper
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%if %mdkversion < 200900
%clean_scrollkeeper
%clean_icon_cache hicolor
%clean_desktop_database
%clean_menus
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS TODO NEWS
%_sysconfdir/gconf/schemas/totem.schemas
%_sysconfdir/gconf/schemas/totem-handlers.schemas
%_sysconfdir/gconf/schemas/totem-video-thumbnail.schemas
%dir %_datadir/omf/totem/
%_datadir/icons/hicolor/*/*/*
%_datadir/omf/totem/totem-C.omf
%_datadir/totem
%_datadir/applications/totem.desktop
%_datadir/gtk-doc/html/%name
%dir %_libdir/totem
%_libdir/totem/plugins/
%_libdir/totem/totem-bugreport.py
%_mandir/man1/*
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_liconsdir}/%name.png
%defattr(-,root,root)
%_bindir/totem
%_bindir/totem-audio-preview
%_bindir/totem-video-indexer
%_bindir/totem-video-thumbnailer


%files nautilus
%defattr(-,root,root)
%_libdir/nautilus/extensions-2.0/*


%if %build_mozilla
%files mozilla
%defattr(-,root,root)
%_libdir/mozilla/plugins/libtotem*.so
%_libexecdir/totem-plugin-viewer
%endif
