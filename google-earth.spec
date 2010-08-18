# TODO:
# - move configs to /etc
# - mark national resources as lang

%define		buildid	1.1547
%define		rel		0.2
Summary:	Google Earth - 3D planet viewer
Summary(pl.UTF-8):	Google Earth - globus
Name:		GoogleEarth
Version:	5.2
Release:	%{buildid}.%{rel}
License:	non distributable - EULA?
Group:		Applications/Graphics
Source0:	http://dl.google.com/earth/client/current/%{name}Linux.bin
# NoSource0-md5:	3d6cc89e17daa361f6087ea495d06a84
NoSource:	0
Source1:	%{name}.desktop
Patch0:		%{name}-decimal_separator.patch
URL:		http://earth.google.com/
Suggests:	fonts-TTF-bitstream-vera
ExclusiveArch:	%{ix86}
Requires:	cpuinfo(sse2)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_libdir}/%{name}

# Mesa-libGLU
%define		mesa_caps		libGLU.so
# QtCore, QtGui, QtNetwork, QtWebKit
%define		qt4_caps		libQtCore.so libQtGui.so libQtNetwork.so libQtWebKit.so
# curl-libs
%define		curl_caps		libcurl.so
# libicu
%define		icu_caps		libicudata.so libicuuc.so

%define		_noautoprov		%{mesa_caps} %{qt4_caps} %{curl_caps} %{icu_caps}
%define		_noautoreq		%{_noautoprov}

%description
Google Earth puts a planet's worth of imagery and other geographic
information right on your desktop. View exotic locales like Maui and
Paris as well as points of interest such as local restaurants,
hospitals, schools, and more.

%description -l pl.UTF-8
Google Earth pokazuje obrazy Ziemi oraz informacje geograficzne. Można
obejrzeć tak egzotyczne lokalizacje jak Maui czy Paryż, jak również
miejsca typu restauracje, szpitale, szkoły i inne.

%prep
%setup -qcT
head -n 376 %{SOURCE0} > %{name}-%{version}.sh
tail -n +377 %{SOURCE0} > %{name}-%{version}.tar.bz2

tar jxvf %{name}-%{version}.tar.bz2
tar xvf googleearth-linux-x86.tar
tar xvf googleearth-data.tar

%patch0 -p1

%build
ver=$(awk '/Google Earth version/{print $NF}' README.linux)
if [ "$ver" != %{version}.%{buildid}-1 ]; then
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

sed '/FindPath()/aGOOGLEEARTH_DATA_PATH="%{_appdir}"
5,40d' bin/googleearth > $RPM_BUILD_ROOT%{_bindir}/googleearth

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a googleearth-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}

install -p googleearth-bin $RPM_BUILD_ROOT%{_appdir}
# It should be located in /etc and marked as config
cp -a *.ini $RPM_BUILD_ROOT%{_appdir}

install -p lib* $RPM_BUILD_ROOT%{_appdir}

cp -a lang plugins resources shaders $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.linux
%attr(755,root,root) %{_bindir}/*
%dir %{_appdir}
%{_appdir}/*.ini
%attr(755,root,root) %{_appdir}/googleearth-bin
%attr(755,root,root) %{_appdir}/*.so*
%dir %{_appdir}/plugins
%dir %{_appdir}/plugins/imageformats
%attr(755,root,root) %{_appdir}/plugins/imageformats/*.so*
%dir %{_appdir}/shaders
%{_appdir}/shaders/*

%dir %{_appdir}/lang
%lang(ar) %{_appdir}/lang/ar.qm
%lang(bg) %{_appdir}/lang/bg.qm
%lang(ca) %{_appdir}/lang/ca.qm
%lang(cs) %{_appdir}/lang/cs.qm
%lang(da) %{_appdir}/lang/da.qm
%lang(de) %{_appdir}/lang/de.qm
%lang(el) %{_appdir}/lang/el.qm
%lang(en) %{_appdir}/lang/en.qm
%lang(es) %{_appdir}/lang/es-419.qm
%lang(es) %{_appdir}/lang/es.qm
%lang(fa) %{_appdir}/lang/fa.qm
%lang(fi) %{_appdir}/lang/fi.qm
%lang(fil) %{_appdir}/lang/fil.qm
%lang(fr) %{_appdir}/lang/fr.qm
%lang(he) %{_appdir}/lang/he.qm
%lang(hi) %{_appdir}/lang/hi.qm
%lang(hr) %{_appdir}/lang/hr.qm
%lang(hu) %{_appdir}/lang/hu.qm
%lang(id) %{_appdir}/lang/id.qm
%lang(it) %{_appdir}/lang/it.qm
%lang(ja) %{_appdir}/lang/ja.qm
%lang(ko) %{_appdir}/lang/ko.qm
%lang(lt) %{_appdir}/lang/lt.qm
%lang(lv) %{_appdir}/lang/lv.qm
%lang(nl) %{_appdir}/lang/nl.qm
%lang(no) %{_appdir}/lang/no.qm
%lang(pl) %{_appdir}/lang/pl.qm
%lang(pt) %{_appdir}/lang/pt-PT.qm
%lang(pt) %{_appdir}/lang/pt.qm
%lang(ro) %{_appdir}/lang/ro.qm
%lang(ru) %{_appdir}/lang/ru.qm
%lang(sk) %{_appdir}/lang/sk.qm
%lang(sl) %{_appdir}/lang/sl.qm
%lang(sr) %{_appdir}/lang/sr.qm
%lang(sv) %{_appdir}/lang/sv.qm
%lang(th) %{_appdir}/lang/th.qm
%lang(tr) %{_appdir}/lang/tr.qm
%lang(uk) %{_appdir}/lang/uk.qm
%lang(vi) %{_appdir}/lang/vi.qm
%lang(zh) %{_appdir}/lang/zh-Hans.qm
%lang(zh_HK) %{_appdir}/lang/zh-Hant-HK.qm
%lang(zh_TW) %{_appdir}/lang/zh-Hant.qm

%dir %{_appdir}/resources
%{_appdir}/resources/*.png
%{_appdir}/resources/*.country
%{_appdir}/resources/*.kml
%{_appdir}/resources/*.rcc
%{_appdir}/resources/doppler.txt
%{_appdir}/resources/flightsim
%{_appdir}/resources/paddle
%{_appdir}/resources/pushpin
%{_appdir}/resources/shapes
%lang(ar) %{_appdir}/resources/ar.locale
%lang(bg) %{_appdir}/resources/bg.locale
%lang(ca) %{_appdir}/resources/ca.locale
%lang(cs) %{_appdir}/resources/cs.locale
%lang(da) %{_appdir}/resources/da.locale
%lang(de) %{_appdir}/resources/de.locale
%lang(el) %{_appdir}/resources/el.locale
%lang(es) %{_appdir}/resources/es-419.locale
%lang(en) %{_appdir}/resources/en.locale
%lang(es) %{_appdir}/resources/es.locale
%lang(fi) %{_appdir}/resources/fi.locale
%lang(fil) %{_appdir}/resources/fil.locale
%lang(fr) %{_appdir}/resources/fr.locale
%lang(he) %{_appdir}/resources/he.locale
%lang(hi) %{_appdir}/resources/hi.locale
%lang(hr) %{_appdir}/resources/hr.locale
%lang(hu) %{_appdir}/resources/hu.locale
%lang(id) %{_appdir}/resources/id.locale
%lang(it) %{_appdir}/resources/it.locale
%lang(ja) %{_appdir}/resources/ja.locale
%lang(ko) %{_appdir}/resources/ko.locale
%lang(lt) %{_appdir}/resources/lt.locale
%lang(lv) %{_appdir}/resources/lv.locale
%lang(nl) %{_appdir}/resources/nl.locale
%lang(no) %{_appdir}/resources/no.locale
%lang(pl) %{_appdir}/resources/pl.locale
%lang(pt) %{_appdir}/resources/pt.locale
%lang(pt_PT) %{_appdir}/resources/pt-PT.locale
%lang(ro) %{_appdir}/resources/ro.locale
%lang(ru) %{_appdir}/resources/ru.locale
%lang(sk) %{_appdir}/resources/sk.locale
%lang(sl) %{_appdir}/resources/sl.locale
%lang(sr) %{_appdir}/resources/sr.locale
%lang(sv) %{_appdir}/resources/sv.locale
%lang(th) %{_appdir}/resources/th.locale
%lang(tr) %{_appdir}/resources/tr.locale
%lang(uk) %{_appdir}/resources/uk.locale
%lang(vi) %{_appdir}/resources/vi.locale
%lang(zh) %{_appdir}/resources/zh-Hans.locale
%lang(zh_TW) %{_appdir}/resources/zh-Hant.locale
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
