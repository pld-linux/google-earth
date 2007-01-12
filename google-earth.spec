#
# TODO:
# - move configs to /etc
# - mark national resources as lang
#
Summary:	Google Earth - 3D planet viewer
Summary(pl):	Google Earth - globus
Name:		GoogleEarth
Version:	4
Release:	0.2723.0
License:	non distributable - EULA?
Group:		Applications/Graphics
Source0:	http://dl.google.com/earth/GE%{version}/%{name}Linux.bin
# NoSource0-md5:	0a97dfa4b22d561799a0131822293fad
NoSource:	0
Source1:	%{name}.desktop
URL:		http://earth.google.com/
Requires:	curl-libs
Requires:	openssl
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_google_data_path	%{_libdir}/%{name}

%description
Google Earth puts a planet's worth of imagery and other geographic
information right on your desktop. View exotic locales like Maui and
Paris as well as points of interest such as local restaurants,
hospitals, schools, and more.

%description -l pl
Google Earth pokazuje obrazy Ziemi oraz informacje geograficzne. Mo¿na
obejrzeæ tak egzotyczne lokalizacje jak Maui czy Pary¿, jak równie¿
miejsca typu restauracje, szpitale, szko³y i inne.

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

cp -R kvw xml lang res resources $RPM_BUILD_ROOT%{_google_data_path}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc EULA-*
%attr(755,root,root) %{_bindir}/*
%dir %{_google_data_path}
%{_google_data_path}/*.ini
%attr(755,root,root) %{_google_data_path}/googleearth-bin
%attr(755,root,root) %{_google_data_path}/*.so*
%dir %{_google_data_path}/kvw
%{_google_data_path}/kvw/*.kvw
%dir %{_google_data_path}/lang
%{_google_data_path}/lang/*.qm
%dir %{_google_data_path}/res
%{_google_data_path}/res/pal*
%{_google_data_path}/res/*.png
%dir %{_google_data_path}/resources
%{_google_data_path}/resources/*.png
%{_google_data_path}/resources/*.jpg
%lang(de) %{_google_data_path}/resources/de.locale
%lang(en) %{_google_data_path}/resources/en.locale
%lang(en_AU) %{_google_data_path}/resources/en_AU.locale
%lang(en_CA) %{_google_data_path}/resources/en_CA.locale
%lang(en_GB) %{_google_data_path}/resources/en_GB.locale
%lang(en_NZ) %{_google_data_path}/resources/en_NZ.locale
%lang(en_US) %{_google_data_path}/resources/en_US.locale
%lang(es) %{_google_data_path}/resources/es.locale
%lang(fr) %{_google_data_path}/resources/fr.locale
%lang(it) %{_google_data_path}/resources/it.locale
%lang(ja) %{_google_data_path}/resources/ja.locale
%dir %{_google_data_path}/xml
%{_google_data_path}/xml/*.xml
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
