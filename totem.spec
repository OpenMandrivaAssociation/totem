%define url_ver %(echo %{version} | cut -d "." -f -2)

# Upstream: https://bugzilla.gnome.org/show_bug.cgi?id=786248
# build randomly failling with: 
# "error: Package `Totem-1.0' not found in specified Vala API directories or GObject-Introspection GIR directories"
%global _smp_ncpus_max 4

%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define api		1.0
%define major		0
%define girmajor	1.0
%define libname		%mklibname %{name} %{major}
%define girname		%mklibname %{name}-gir %{girmajor}
%define develname	%mklibname %{name} -d

Summary:	Movie player for GNOME
Name:		totem
Version:	43.2
Release:	1
License:	GPLv2 with exception
Group:		Video
URL:		https://projects.gnome.org/totem/
Source0:	https://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
#(nl) KDE Solid integration : from mdv svn  soft/mandriva-kde-translation/trunk/solid/
Source1:	totem-opendvd.desktop

BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	shared-mime-info
#BuildRequires:	python-pylint
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd45-xml
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	gstreamer1.0-plugins-good
BuildRequires:	gstreamer1.0-plugins-bad
BuildRequires:	gstreamer1.0-soundtouch
BuildRequires:	gstreamer1.0-soup
BuildRequires:	gstreamer1.0-tools
BuildRequires:	pkgconfig(gstreamer-audio-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	gstreamer1.0-gtk
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	vala
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk+-x11-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.6.8
BuildRequires:	pkgconfig(clutter-gst-3.0) >= 2.99.2
BuildRequires:	pkgconfig(clutter-gtk-1.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(grilo-0.3) >= 0.2.0
BuildRequires:	pkgconfig(grilo-pls-0.3)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libhandy-1)
BuildRequires:	pkgconfig(libportal-gtk3)
BuildRequires:	pkgconfig(libepc-ui-1.0) > 0.4.0
BuildRequires:	pkgconfig(libgdata) >= 0.4.0
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(libpeas-gtk-1.0) >= 0.7.2
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(shared-mime-info)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(adwaita-icon-theme)
#BuildRequires:	pkgconfig(clutter-gst-2.0)
BuildRequires:	pkgconfig(totem-plparser)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(zeitgeist-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	meson
BuildRequires:	libxml2-utils
BuildRequires:	yelp-tools

%ifarch %{ix86} x86_64
BuildRequires:	pkgconfig(nvtvsimple)
%endif

Requires:	grilo-plugins
Requires:	iso-codes
Requires:	gstreamer1.0-plugins-base
Requires:	gstreamer1.0-plugins-good
Requires:	gstreamer1.0-soup
Requires:	gstreamer1.0-libav
Requires:	gstreamer1.0-gtk
Recommends:	gstreamer1.0-resindvd
Recommends:	gstreamer1.0-a52dec
# Must have plugins. Totem doesn't start without them
Requires:	gstreamer1.0-gstclutter3
Requires:	gstreamer1.0-soundtouch

#gw opensubtitles plugin:
Requires:	pyxdg
# python plugins
Requires:	python-dbus
Requires:	python-gi

Obsoletes:	%{name}-tracker < 3.4
Obsoletes:      totem-nautilus < 3.30.0-2

%description
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

%package -n %{libname}
Group:		System/Libraries
Summary:	Shared libraries for %{name}

%description -n %{libname}
This package contains the shared libraries for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Group:		Development/C
Summary:	Devel files for %{name}
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Devel files for %{name}.
%prep
%autosetup -p1

%build
%meson -Denable-gtk-doc=true
%meson_build

%install
%meson_install

%find_lang %{name} --with-gnome

#menu
MIME_TYPES=`tr '\n' , < data/mime-type-list.txt | sed -e 's/,$//'`
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="X-MandrivaLinux-Multimedia-Video" \
	--add-category="X-MandrivaLinux-CrossDesktop" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

#(nl) KDE Solid integration
mkdir -p %{buildroot}/%{_datadir}/apps/solid/actions
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/apps/solid/actions/

%files -f %{name}.lang
%doc README AUTHORS NEWS
%{_bindir}/totem
%{_bindir}/totem-video-thumbnailer
%dir %{_libdir}/totem
%dir %{_libdir}/totem/plugins/
%dir %{_libdir}/totem/plugins/im-status
%dir %{_libdir}/totem/plugins/save-file
%{_libdir}/totem/plugins/im-status/*
%{_libdir}/totem/plugins/mpris/libmpris.so
%{_libdir}/totem/plugins/mpris/mpris.plugin
%{_libdir}/totem/plugins/opensubtitles
%{_libdir}/totem/plugins/properties
%{_libdir}/totem/plugins/autoload-subtitles
%{_libdir}/totem/plugins/recent
%{_libdir}/totem/plugins/pythonconsole
%{_libdir}/totem/plugins/rotation
%{_libdir}/totem/plugins/save-file/*
%{_libdir}/totem/plugins/screensaver
%{_libdir}/totem/plugins/screenshot
%{_libdir}/totem/plugins/skipto
%{_libdir}/totem/plugins/variable-rate/libvariable-rate.so
%{_libdir}/totem/plugins/variable-rate/variable-rate.plugin
%{_libdir}/totem/plugins/open-directory/libopen-directory.so
%{_libdir}/totem/plugins/open-directory/open-directory.plugin
%{_datadir}/metainfo/org.gnome.Totem.appdata.xml
%{_datadir}/applications/org.gnome.Totem.desktop
%{_datadir}/apps/solid/actions/totem-opendvd.desktop
%{_datadir}/dbus-1/services/org.gnome.Totem.service
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/thumbnailers/totem.thumbnailer
%{_libexecdir}/totem-gallery-thumbnailer
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libtotem.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Totem-1.0.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_libdir}/libtotem.so
%{_libdir}/pkgconfig/totem.pc
%{_includedir}/totem/%{api}/*
%{_datadir}/gir-1.0/Totem-1.0.gir
