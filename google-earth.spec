# TODO:
# - move configs to /etc
Summary:	Google Earth - 3D planet viewer
Summary(pl.UTF-8):	Google Earth - globus
Name:		google-earth
Version:	7.1.4.1529
Release:	0.1
License:	Multiple, see http://www.google.com/earth
Group:		Applications/Graphics
Obsoletes:	GoogleEarth
Source0:	http://dl.google.com/dl/earth/client/current/%{name}-stable_current_i386.rpm
# NoSource0-md5:	
NoSource:	0
Source1:        http://dl.google.com/dl/earth/client/current/%{name}-stable_current_x86_64.rpm
# NoSource1-md5:	
NoSource:	1
Source2:	%{name}.desktop
Patch0:		decimal_separator.patch
URL:		http://www.google.com/earth
BuildRequires:	rpm-utils
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	sed >= 4.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	cpuinfo(sse2)
# for /lib/ld-lsb.so.3
Requires:	lsb-release >= 4.0
Suggests:	fonts-TTF-bitstream-vera
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libGLU.so.1

%define		_appdir		%{_libdir}/%{name}

# Qt4 plugins
%define		_noautoprovfiles	%{_libdir}/%{name}/plugins/imageformats

# Mesa-libGLU
%define		mesa_caps		libGLU.so
# QtCore, QtGui, QtNetwork, QtWebKit
%define		qt4_caps		libQtCore.so libQtGui.so libQtNetwork.so libQtWebKit.so
# curl-libs
%define		curl_caps		libcurl.so
# libicu
%define		icu_caps		libicudata.so libicuuc.so
# nss_mdns
%define		mdns_caps		libnss_mdns4_minimal.so.2
# proj
%define		proj_caps		libproj.so.0
# expat
%define		expat_caps		libexpat.so.1
# nss
%define		nss_caps		libfreebl3.so libssl3.so libsoftokn3.so libsmime3.so libnss3.so libnssckbi.so libnssdbm3.so libnssutil3.so
# nspr
%define		nspr_caps		libnspr4.so libplc4.so libplds4.so
# sqlite3
%define		sqlite_caps		libsqlite3.so
# gdal
%define		gdal_caps		libgdal.so.1
# gdata
%define		gdata_caps		libgdata.so

# check with:
# cd lib; for a in *.so*; do ls -ld /lib*/$a /usr/lib*/$a; done 2>/dev/null

%define		_noautoprov		%{mesa_caps} %{qt4_caps} %{curl_caps} %{icu_caps} %{mdns_caps} %{proj_caps} %{expat_caps} %{nss_caps} %{nspr_caps} %{sqlite_caps} %{gdal_caps} %{gdata_caps}
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
%ifarch %{ix86}
SOURCE=%{S:0}
%endif
%ifarch %{x8664}
SOURCE=%{S:1}
%endif

V=$(rpm -qp --nodigest --nosignature --qf '%{V}' $SOURCE)
if [ "$V" != "%{version}" ]; then
	exit 1
fi
rpm2cpio $SOURCE | cpio -i -d

mv opt/google/earth/free lib
# doc stuff
mv lib/gpl.txt .

# bin dir stuff
rm lib/google-earth

# isolate desktop stuff, we install them differently
install -d desktop
mv lib/product_logo_* desktop
mv lib/google-earth.desktop desktop

# we place stuff already to proper dir by package
rm lib/xdg-settings
rm lib/xdg-mime

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}

cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/googleearth $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
for icon in desktop/product_logo_*.png; do
	size=${icon##*/product_logo_} size=${size%.png}
	dir=$RPM_BUILD_ROOT%{_iconsdir}/hicolor/${size}x${size}/apps
	install -d $dir
	cp -a $icon $dir/%{name}.png
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/google-earth
%{_desktopdir}/google-earth.desktop
%{_iconsdir}/hicolor/*/apps/google-earth.png
%dir %{_appdir}
%{_appdir}/*.ini
%{_appdir}/kh20
%attr(755,root,root) %{_appdir}/googleearth-bin
%attr(755,root,root) %{_appdir}/googleearth
%attr(755,root,root) %{_appdir}/gpsbabel
%attr(755,root,root) %{_appdir}/*.so*
%dir %{_appdir}/plugins
%dir %{_appdir}/plugins/imageformats
%attr(755,root,root) %{_appdir}/plugins/libnpgeinprocessplugin.so
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
%{_appdir}/resources/*.kml
%{_appdir}/resources/*.rcc
%{_appdir}/resources/doppler.txt
%{_appdir}/resources/flightsim
