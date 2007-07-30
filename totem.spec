%define major 7
%define lib_name %mklibname totem-plparser %major
%define build_gstreamer 1
%define build_xine 1
%{?_with_gstreamer: %{expand: %%global build_gstreamer 1}}
%{?_without_gstreamer: %{expand: %%global build_gstreamer 0}}
%define build_mozilla 1

%define xineversion 1.1.2
%define gstver 0.10

Summary: Movie player for GNOME 2
Name: totem
Version: 2.19.6
Release: %mkrel 1
Source0: http://ftp.gnome.org/pub/GNOME/sources/totem/%{name}-%{version}.tar.bz2
Source1: %name-48.png
License: GPL
Group: Video
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://www.hadess.net/totem.php3
%if %build_gstreamer
BuildRequires: libgstreamer-plugins-base-devel >= %gstver
BuildRequires: gstreamer0.10-plugins-good
BuildRequires: gstreamer0.10-plugins-base
%endif
BuildRequires: libxdmcp-devel
BuildRequires: libxtst-devel
BuildRequires: libxxf86vm-devel
BuildRequires: libxine-devel >= %xineversion
BuildRequires: libnvtvsimple-devel
BuildRequires: scrollkeeper
BuildRequires: gnome-doc-utils
BuildRequires: liblirc-devel
BuildRequires: libnautilus-devel
BuildRequires: libgalago-devel
BuildRequires: libvala-devel
BuildRequires: libbluez-devel
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
Requires: pygtk2.0
Requires: xine-plugins >= %xineversion
Requires: totem-common = %{version}-%{release}
Provides: totem-bin = %{version}-%{release}


%description
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.
This version is based on the xine backend.

#gw TODO: obsolete totem-gstreamer in main totem package and move the xine
#gw backend to a totem-xine package
%if %build_gstreamer
%package gstreamer
Summary: %{summary}
Group:	Video
Requires: gstreamer0.10-plugins-base >= %gstver
Requires: gstreamer0.10-plugins-good
Requires: totem-common = %{version}
Provides: totem-bin = %{version}-%{release}
#Requires: gstreamer0.10-ffmpeg >= %gstver
#Suggests: gstreamer0.10-flac >= %gstver
#Suggests: gstreamer0.10-faad >= %gstver

%description gstreamer
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

This version is based on the gstreamer backend.

%if %build_mozilla
%package mozilla-gstreamer
Summary: Totem video plugin for Mozilla Firefox - gstreamer backend
Group: Networking/WWW
BuildRequires: mozilla-firefox-devel
BuildRequires: dbus-devel >= 0.35
%define firefox_version %(rpm -q mozilla-firefox --queryformat %{VERSION})
Requires: %mklibname mozilla-firefox %{firefox_version}
Requires: totem-gstreamer = %version

%description mozilla-gstreamer
This embeds the Totem video player into web browsers based on Mozilla
Firefox. This version is based on the gstreamer backend.
%endif
%endif

%package common
Summary: Common data files for totem 
Group:	Video
Requires: iso-codes
Requires(post)  : scrollkeeper >= 0.3 desktop-file-utils
Requires(postun): scrollkeeper >= 0.3 desktop-file-utils
Requires: totem-bin = %version

%description common
Common data files used by Totem.

%package -n	%{lib_name}
Summary:	%{summary}
Group:		System/Libraries

%description -n	%{lib_name}
Shared library used by totem.

%package -n	%{lib_name}-devel
Summary:	Static libraries, include files for totem playlist parser
Group:		Development/GNOME and GTK+
Provides:	totem-plparser-devel = %{version}
Provides:	libtotem-plparser-devel = %{version}
Requires:	%{lib_name} = %{version}
Conflicts: 	%{_lib}totem-plparser0-devel

%description -n	%{lib_name}-devel
Static libraries, include files for totem playlist parser

%if %build_mozilla
%package mozilla
Summary: Totem video plugin for Mozilla Firefox
Group: Networking/WWW
BuildRequires: mozilla-firefox-devel
BuildRequires: dbus-devel >= 0.35
Requires: %mklibname mozilla-firefox %{firefox_version}
Requires: totem = %version

%description mozilla
This embeds the Totem video player into web browsers based on Mozilla Firefox.
This version is based on the xine backend.
%endif

%prep
%setup -q
aclocal
autoconf
automake

%build

# Build xine version
[ -d xine-build ] || mkdir xine-build
cd xine-build

CONFIGURE_TOP=.. %configure2_5x --disable-run-in-source-tree \
%if %build_mozilla
--enable-mozilla \
%else
--disable-mozilla \
%endif
--enable-xine
%make
cd ..

%if %build_gstreamer
# Build gstreamer version
[ -d gstreamer-build ] || mkdir gstreamer-build
cd gstreamer-build

CONFIGURE_TOP=.. %configure2_5x --disable-run-in-source-tree \
%if %build_mozilla
--enable-mozilla \
%else
--disable-mozilla
%endif

%make
cd ..
%endif


%install
rm -rf $RPM_BUILD_ROOT %name.lang

cd xine-build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
%if %build_mozilla
mv %buildroot%_libdir/mozilla/plugins/libtotem-basic-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-basic-plugin-xine.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-complex-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-complex-plugin-xine.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-gmp-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-gmp-plugin-xine.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-mully-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-mully-plugin-xine.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-narrowspace-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-narrowspace-plugin-xine.so

mv %buildroot%_libexecdir/totem-plugin-viewer %buildroot%_libexecdir/totem-plugin-viewer-xine
%endif
cd ..
mv $RPM_BUILD_ROOT%{_bindir}/totem $RPM_BUILD_ROOT%{_bindir}/totem-xine
mv $RPM_BUILD_ROOT%{_bindir}/totem-video-thumbnailer $RPM_BUILD_ROOT%{_bindir}/totem-video-thumbnailer-xine
mv $RPM_BUILD_ROOT%{_bindir}/totem-video-indexer $RPM_BUILD_ROOT%{_bindir}/totem-video-indexer-xine
mv $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/libtotem-properties-page.so $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/libtotem-properties-page-xine 


%if %build_gstreamer
cd gstreamer-build
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
%if %build_mozilla
mv %buildroot%_libdir/mozilla/plugins/libtotem-basic-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-basic-plugin-gstreamer.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-complex-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-complex-plugin-gstreamer.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-gmp-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-gmp-plugin-gstreamer.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-mully-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-mully-plugin-gstreamer.so
mv %buildroot%_libdir/mozilla/plugins/libtotem-narrowspace-plugin.so %buildroot%_libdir/mozilla/plugins/libtotem-narrowspace-plugin-gstreamer.so
mv %buildroot%_libexecdir/totem-plugin-viewer %buildroot%_libexecdir/totem-plugin-viewer-gstreamer
%endif
cd ..
mv $RPM_BUILD_ROOT%{_bindir}/totem $RPM_BUILD_ROOT%{_bindir}/totem-gstreamer
mv $RPM_BUILD_ROOT%{_bindir}/totem-video-thumbnailer $RPM_BUILD_ROOT%{_bindir}/totem-video-thumbnailer-gstreamer
mv $RPM_BUILD_ROOT%{_bindir}/totem-video-indexer $RPM_BUILD_ROOT%{_bindir}/totem-video-indexer-gstreamer
mv $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/libtotem-properties-page.so $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/libtotem-properties-page-gstreamer
%endif

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

#menu
MIME_TYPES=`tr '\n' , < data/mime-type-list.txt | sed -e 's/,$//'`
install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/%{name}-xine" \
	needs="X11" \
	section="Multimedia/Video" \
	icon="totem.png" \
	mimetypes="$MIME_TYPES,audio/basic,video/x-m4v" \
	accept_url="true" \
	multiple_files="true" \
	title="Totem Movie Player" \
	longtitle="Play movies and songs" \
	startup_notify="true" \
	kde_opt="InitialPreference=10" xdg="true"
?package(%{name}): \
	command="%{_bindir}/%{name}-xine" \
	needs="X11" \
	section="Multimedia/Sound" \
	icon="totem.png" \
	title="Totem Media Player" \
	longtitle="Play movies and songs" \
	startup_notify="true" \
	kde_opt="InitialPreference=10" xdg="true"

EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%if %build_gstreamer
cat $RPM_BUILD_ROOT%{_menudir}/%{name} | sed -e 's/xine/gstreamer/g' -e 's/package(totem)/package(totem-gstreamer)/g' > $RPM_BUILD_ROOT%{_menudir}/%{name}-gstreamer
%endif

#icons
mkdir -p %buildroot{%_liconsdir,%_miconsdir,%_iconsdir}
mkdir -p %buildroot%_iconsdir/hicolor/48x48/apps
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%name.png
install -D -m 644 data/icons/16x16/totem.png $RPM_BUILD_ROOT%{_miconsdir}/%name.png
install -D -m 644 data/icons/32x32/totem.png $RPM_BUILD_ROOT%{_iconsdir}/%name.png
install -D -m 644 %{SOURCE1} %buildroot/%_liconsdir/%name.png


# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/{totem/plugins/*/,mozilla/plugins,nautilus/extensions-1.0}/*.{la,a} %buildroot/var/lib/scrollkeeper 

%clean
rm -rf $RPM_BUILD_ROOT

%post common
%update_scrollkeeper
%define schemas totem totem-video-thumbnail totem-handlers
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%update_desktop_database

%post
update-alternatives --install %{_bindir}/totem totem /usr/bin/totem-xine 20 --slave %{_libdir}/nautilus/extensions-1.0/libtotem-properties-page.so totem_nautilus_properties %{_libdir}/nautilus/extensions-1.0/libtotem-properties-page-xine --slave %{_bindir}/totem-video-thumbnailer totem-video-thumbnailer /usr/bin/totem-video-thumbnailer-xine --slave %{_bindir}/totem-video-indexer totem-video-indexer /usr/bin/totem-video-indexer-xine 
%{update_menus}

%if %build_mozilla
%post mozilla
update-alternatives --install %{_libexecdir}/totem-plugin-viewer totem-mozilla %{_libexecdir}/totem-plugin-viewer-xine 20
%endif

%preun common
%preun_uninstall_gconf_schemas %schemas

%postun common
%clean_scrollkeeper
%clean_icon_cache hicolor
%clean_desktop_database

%triggerpostun -- totem-mozilla < 2.18.0-2mdv, totem-mozilla-gstreamer < 2.18.0-2mdv
update-alternatives --auto totem-mozilla

%postun
if [ "$1" = "0" ]; then
  update-alternatives --remove totem /usr/bin/totem-xine 
fi
%{clean_menus}

%if %build_mozilla
%postun mozilla
if [ "$1" = "0" ]; then
  update-alternatives --remove totem-plugin-viewer %_libexecdir/totem-plugin-viewer-xine
fi
%endif

%triggerpostun -- totem < 1.0.1-2mdk
update-alternatives --auto totem


%if %build_gstreamer
%post gstreamer
update-alternatives --install %{_bindir}/totem totem /usr/bin/totem-gstreamer 10 --slave %{_libdir}/nautilus/extensions-1.0/libtotem-properties-page.so totem_nautilus_properties %{_libdir}/nautilus/extensions-1.0/libtotem-properties-page-gstreamer --slave %{_bindir}/totem-video-thumbnailer totem-video-thumbnailer /usr/bin/totem-video-thumbnailer-gstreamer --slave %{_bindir}/totem-video-indexer totem-video-indexer /usr/bin/totem-video-indexer-gstreamer
%{update_menus}
%if %build_mozilla
%post mozilla-gstreamer
update-alternatives --install %{_libexecdir}/totem-plugin-viewer totem-mozilla %{_libexecdir}/totem-plugin-viewer-gstreamer 10
%endif

%postun gstreamer
if [ "$1" = "0" ]; then
  update-alternatives --remove totem /usr/bin/totem-gstreamer
fi
%{clean_menus}
%if %build_mozilla
%postun mozilla-gstreamer
if [ "$1" = "0" ]; then
  update-alternatives --remove totem-plugin-viewer %_libexecdir/totem-plugin-viewer-gstreamer
fi
%endif
%endif

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

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
%if %build_mozilla
%_libdir/mozilla/plugins/*.xpt
%endif
%_mandir/man1/*
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%{_liconsdir}/%name.png

%files 
%defattr(-,root,root)
%_bindir/*-xine
%_libdir/nautilus/extensions-1.0/*-xine
%_menudir/%name

%if %build_gstreamer
%files gstreamer
%defattr(-,root,root)
%_bindir/*-gstreamer
%_libdir/nautilus/extensions-1.0/*-gstreamer
%_menudir/%name-gstreamer
%if %build_mozilla
%files mozilla-gstreamer
%defattr(-,root,root)
%_libdir/mozilla/plugins/libtotem*gstreamer.so
%_libexecdir/totem-plugin-viewer-gstreamer
%endif
%endif

%if %build_mozilla
%files mozilla
%defattr(-,root,root)
%_libdir/mozilla/plugins/libtotem*xine.so
%_libexecdir/totem-plugin-viewer-xine
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libtotem-plparser.so.%{major}*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_includedir}/totem
%{_libdir}/pkgconfig/*


