#
# TODO:
# - move configs to /etc
# - mark national resources as lang
#
Summary:	Google Earth - 3D planet viewer
Summary(pl.UTF-8):	Google Earth - globus
Name:		GoogleEarth
Version:	5
Release:	1.3509.4636
License:	non distributable - EULA?
Group:		Applications/Graphics
Source0:	http://dl.google.com/earth/client/current/%{name}Linux.bin
# NoSource0-md5:	ec0491757d3627cd3981f390b093596b
NoSource:	0
Source1:	%{name}.desktop
URL:		http://earth.google.com/
Suggests:	fonts-TTF-bitstream-vera
ExclusiveArch:	%{ix86}
Requires:	cpuinfo(sse2)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_google_data_path	%{_libdir}/%{name}
%define		_noautoprov		^\\./ ^libGLU\\.so ^libcrypto\\.so \
	^libcurl\\.so ^libicudata\\.so ^libicuuc\\.so ^libfreeimage\\.so \
	^libgcc_s\\.so ^libjpeg\\.so ^libmng\\.so ^libpng12\\.so \
	^libqt-mt\\.so ^libqui\\.so ^libssl\\.so ^libstdc++\\.so \
	^libtiff\\.so ^libz\\.so
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
%setup -q -T -c
head -n 376 %{SOURCE0} > %{name}-%{version}.sh
tail -n +377 %{SOURCE0} > %{name}-%{version}.tar.bz2

tar -jxvf %{name}-%{version}.tar.bz2
tar -xvf googleearth-linux-x86.tar
tar -xvf googleearth-data.tar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_google_data_path}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

sed '/FindPath()/aGOOGLEEARTH_DATA_PATH="%{_google_data_path}"
5,40d' bin/googleearth > $RPM_BUILD_ROOT%{_bindir}/googleearth

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install googleearth-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}

install googleearth-bin $RPM_BUILD_ROOT%{_google_data_path}
# It should be located in /etc and marked as config
install *.ini $RPM_BUILD_ROOT%{_google_data_path}

# Some libraries:
#install libcomponent.so libfusion.so libgeobase.so libmath.so \
#	libwmsbase.so libnet.so libcollada.so libbase.so libgoogleearth.so \
#	$RPM_BUILD_ROOT%{_google_data_path}
#install lib{IGAttrs,IGCollision,IGCore,IGDisplay,IGExportCommon,IGGfx,IGGui,IGMath,IGOpt,IGSg,IGUtils,auth,common,framework,render,evll}.so \
#	lib{navigate,layer,measure,gps,basicIngest,googlesearch}.so \
#	$RPM_BUILD_ROOT%{_google_data_path}
#install lib{freeimage.so.3,{crypto,ssl}.so.0.9.8} $RPM_BUILD_ROOT%{_libdir}
install lib* $RPM_BUILD_ROOT%{_google_data_path}

cp -R lang plugins resources shaders $RPM_BUILD_ROOT%{_google_data_path}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.linux
%attr(755,root,root) %{_bindir}/*
%dir %{_google_data_path}
%{_google_data_path}/*.ini
%attr(755,root,root) %{_google_data_path}/googleearth-bin
%attr(755,root,root) %{_google_data_path}/*.so*
%dir %{_google_data_path}/plugins
%dir %{_google_data_path}/plugins/imageformats
%attr(755,root,root) %{_google_data_path}/plugins/imageformats/*.so*
%dir %{_google_data_path}/shaders
%{_google_data_path}/shaders/*

%dir %{_google_data_path}/lang
%{_google_data_path}/lang/*.qm
%dir %{_google_data_path}/resources
%{_google_data_path}/resources/*.png
#%{_google_data_path}/resources/*.jpg
%{_google_data_path}/resources/*.country
%{_google_data_path}/resources/*.kml
%{_google_data_path}/resources/*.rcc
%{_google_data_path}/resources/doppler.txt
%{_google_data_path}/resources/flightsim
%{_google_data_path}/resources/paddle
%{_google_data_path}/resources/pushpin
%{_google_data_path}/resources/shapes
%lang(ar) %{_google_data_path}/resources/ar.locale
%lang(bg) %{_google_data_path}/resources/bg.locale
%lang(ca) %{_google_data_path}/resources/ca.locale
%lang(cs) %{_google_data_path}/resources/cs.locale
%lang(da) %{_google_data_path}/resources/da.locale
%lang(de) %{_google_data_path}/resources/de.locale
%lang(el) %{_google_data_path}/resources/el.locale
%lang(es) %{_google_data_path}/resources/es-419.locale
%lang(en) %{_google_data_path}/resources/en.locale
%lang(es) %{_google_data_path}/resources/es.locale
%lang(fi) %{_google_data_path}/resources/fi.locale
%lang(fil) %{_google_data_path}/resources/fil.locale
%lang(fr) %{_google_data_path}/resources/fr.locale
%lang(he) %{_google_data_path}/resources/he.locale
%lang(hi) %{_google_data_path}/resources/hi.locale
%lang(hr) %{_google_data_path}/resources/hr.locale
%lang(hu) %{_google_data_path}/resources/hu.locale
%lang(id) %{_google_data_path}/resources/id.locale
%lang(it) %{_google_data_path}/resources/it.locale
%lang(ja) %{_google_data_path}/resources/ja.locale
%lang(ko) %{_google_data_path}/resources/ko.locale
%lang(lt) %{_google_data_path}/resources/lt.locale
%lang(lv) %{_google_data_path}/resources/lv.locale
%lang(nl) %{_google_data_path}/resources/nl.locale
%lang(no) %{_google_data_path}/resources/no.locale
%lang(pl) %{_google_data_path}/resources/pl.locale
%lang(pt) %{_google_data_path}/resources/pt.locale
%lang(pt_PT) %{_google_data_path}/resources/pt-PT.locale
%lang(ro) %{_google_data_path}/resources/ro.locale
%lang(ru) %{_google_data_path}/resources/ru.locale
%lang(sk) %{_google_data_path}/resources/sk.locale
%lang(sl) %{_google_data_path}/resources/sl.locale
%lang(sr) %{_google_data_path}/resources/sr.locale
%lang(sv) %{_google_data_path}/resources/sv.locale
%lang(th) %{_google_data_path}/resources/th.locale
%lang(tr) %{_google_data_path}/resources/tr.locale
%lang(uk) %{_google_data_path}/resources/uk.locale
%lang(vi) %{_google_data_path}/resources/vi.locale
%lang(zh) %{_google_data_path}/resources/zh-Hans.locale
%lang(zh_TW) %{_google_data_path}/resources/zh-Hant.locale
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
