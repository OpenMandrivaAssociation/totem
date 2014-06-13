%define build_mozilla 1
%define _disable_ld_no_undefined 1

%define api		1.0
%define major		0
%define girmajor	1.0
%define libname		%mklibname %{name} %{major}
%define girname		%mklibname %{name}-gir %{girmajor}
%define develname	%mklibname %{name} -d

Summary:	Movie player for GNOME
Name:		totem
Version:	3.6.3
Release:	8
License:	GPLv2 with exception
Group:		Video
URL:		http://projects.gnome.org/totem/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.6/%{name}-%{version}.tar.xz
#(nl) KDE Solid integration : from mdv svn  soft/mandriva-kde-translation/trunk/solid/
Source1:	totem-opendvd.desktop

BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd45-xml
BuildRequires:	gstreamer1.0-plugins-good
BuildRequires:	gstreamer1.0-plugins-bad
BuildRequires:	gstreamer1.0-soup
BuildRequires:	gstreamer1.0-tools
BuildRequires:	gnome-common
BuildRequires:	intltool
#BuildRequires:	pylint
BuildRequires:	vala
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.6.8
BuildRequires:	pkgconfig(clutter-gst-2.0) >= 1.3.9
BuildRequires:	pkgconfig(clutter-gtk-1.0)
BuildRequires:	pkgconfig(grilo-0.2) >= 0.2.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libepc-ui-1.0) > 0.4.0
BuildRequires:	pkgconfig(libgdata) >= 0.4.0
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(libnautilus-extension) >= 2.91.3
BuildRequires:	pkgconfig(libpeas-gtk-1.0) >= 0.7.2
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(mx-1.0)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(shared-mime-info)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gnome-icon-theme)
BuildRequires:	pkgconfig(clutter-gst-2.0)
BuildRequires:	pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:	pkgconfig(totem-plparser) >= 2.32.4
BuildRequires:	gstreamer1.0-soundtouch
BuildRequires:	pkgconfig(zeitgeist-1.0)
%ifarch %{ix86} x86_64
BuildRequires:	pkgconfig(nvtvsimple)
%endif

Requires:	grilo-plugins
Requires:	iso-codes
Requires:	gstreamer1.0-plugins-base
Requires:	gstreamer1.0-plugins-good
Requires:	gstreamer1.0-soup
Suggests:	gstreamer1.0-resindvd
Suggests:	gstreamer1.0-a52dec
# Must have plugins. Totem doesn't start without them
Requires:	gstreamer1.0-gstclutter
Requires:	gstreamer1.0-soundtouch 

#gw opensubtitles plugin:
Requires:	pyxdg
# python plugins
Requires:	python-dbus
Requires:	python-gi

#gw needed by the iplayer plugin
Requires:	python-httplib2
Requires:	python-feedparser
Requires:	python-beautifulsoup

Obsoletes:	%{name}-tracker < 3.4

%description
Totem is simple movie player for the GNOME desktop. It
features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

%if %{build_mozilla}
%package	mozilla
Summary:	Totem video plugin for Mozilla Firefox
Group:		Networking/WWW
BuildRequires:	pkgconfig(dbus-1)
Obsoletes:	totem-mozilla-gstreamer < %{version}-%{release}
Provides:	totem-mozilla-gstreamer = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description mozilla
This embeds the Totem video player into web browsers based on Mozilla Firefox.
%endif

%package nautilus
Group:		Video
Summary:	Video and Audio Properties tab for Nautilus
#gw just for the translations:
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description nautilus
A Nautilus extension that shows the properties of audio and video
files in the properties dialogue.

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
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--disable-run-in-source-tree \
	--disable-vegas-plugin \
	--enable-easy-codec-installation \
%if %{build_mozilla}
	--enable-browser-plugins \
%else
	--disable-browser-plugins \
%endif

%make

%install
%makeinstall_std
find %{buildroot} -name '*.la' -exec rm -f {} ';'
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
%doc README AUTHORS TODO NEWS
%{_bindir}/totem
%{_bindir}/totem-audio-preview
%{_bindir}/totem-video-thumbnailer
%dir %{_libdir}/totem
%dir %{_libdir}/totem/plugins/
%dir %{_libdir}/totem/plugins/grilo
%dir %{_libdir}/totem/plugins/im-status
%dir %{_libdir}/totem/plugins/save-file
%{_libdir}/totem/plugins/brasero-disc-recorder
%{_libdir}/totem/plugins/chapters
%{_libdir}/totem/plugins/dbus
%{_libdir}/totem/plugins/grilo/*
%{_libdir}/totem/plugins/gromit
%{_libdir}/totem/plugins/im-status/*
%{_libdir}/totem/plugins/lirc
%{_libdir}/totem/plugins/media-player-keys
%{_libdir}/totem/plugins/ontop
%{_libdir}/totem/plugins/opensubtitles
%{_libdir}/totem/plugins/properties
%{_libdir}/totem/plugins/apple-trailers
%{_libdir}/totem/plugins/autoload-subtitles
%{_libdir}/totem/plugins/recent
%{_libdir}/totem/plugins/pythonconsole
%{_libdir}/totem/plugins/rotation
%{_libdir}/totem/plugins/save-file/*
%{_libdir}/totem/plugins/screensaver
%{_libdir}/totem/plugins/screenshot
%{_libdir}/totem/plugins/skipto
%{_libdir}/totem/plugins/zeitgeist-dp
%{_libdir}/totem/totem-bugreport.py
%{_datadir}/applications/totem.desktop
%{_datadir}/apps/solid/actions/totem-opendvd.desktop
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/thumbnailers/totem.thumbnailer
%{_datadir}/totem
%{_mandir}/man1/*

%files nautilus
%{_libdir}/nautilus/extensions-3.0/*

%if %{build_mozilla}
%files mozilla
%{_libdir}/mozilla/plugins/libtotem*.so
%{_libexecdir}/totem-plugin-viewer
%endif

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
