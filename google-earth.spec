#
# TODO:
# - move configs to /etc
# - mark national resources as lang
#
Summary:	Google Earth - 3D planet viewer
Name:		GoogleEarth
Version:	4
Release:	0.5
License:	non distributable - EULA?
Group:		Applications/Graphics
Source0:	http://dl.google.com/earth/GE%{version}/%{name}Linux.bin
# NoSource0-md5:	8a20af712531bdd358dfc738be605d8a
NoSource:	0
Source1:	%{name}.desktop
URL:		http://earth.google.com/
#BuildRequires:	rpm-build >= 4.3-0.20040107.21
#BuildRequires:	rpmbuild(macros) >= 1.236
Requires:	curl-libs
Requires:	openssl
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_google_data_path	%{_libdir}/%{name}

%description
Google Earth puts a planet's worth of imagery and other geographic information right on your desktop. View exotic locales like Maui and Paris as well as points of interest such as local restaurants, hospitals, schools, and more.

%prep
%setup -q -T -c
head -376 %{SOURCE0} > %{name}-%{version}.sh
tail +377 %{SOURCE0} > %{name}-%{version}.tar.bz2

tar -jxvf %{name}-%{version}.tar.bz2
tar -xvf googleearth-linux-x86.tar
tar -xvf googleearth-data.tar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/env.d,%{_bindir},%{_google_data_path}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
#install -d $RPM_BUILD_ROOT{%{jredir},%{_javadir},%{_includedir}} \
#	$RPM_BUILD_ROOT{%{_mandir}/{,ja/}man1,/etc/env.d,%{_prefix}/src/%{name}-sources} \

install bin/googleearth $RPM_BUILD_ROOT%{_bindir}

cat << EOF > $RPM_BUILD_ROOT/etc/env.d/GOOGLEEARTH_DATA_PATH
GOOGLEEARTH_DATA_PATH="%{_google_data_path}"
EOF

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install googleearth-icon.png $RPM_BUILD_ROOT%{_pixmapsdir}

install googleearth-bin $RPM_BUILD_ROOT%{_google_data_path}
# It should be located in /etc and marked as config
install *.ini $RPM_BUILD_ROOT%{_google_data_path}

# Some libraries:
install libcomponent.so libfusion.so libgeobase.so libmath.so \
	libwmsbase.so libnet.so libcollada.so libbase.so libgoogleearth.so \
	$RPM_BUILD_ROOT%{_google_data_path}

cp -R kvw xml lang res resources $RPM_BUILD_ROOT%{_google_data_path}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc EULA-*
%attr(644,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/*
%attr(755,root,root) %{_bindir}/*
%dir %{_google_data_path}
%{_google_data_path}/*.ini
%attr(755,root,root) %{_google_data_path}/googleearth-bin
%attr(755,root,root) %{_google_data_path}/*.so
%dir %{_google_data_path}/kvw
%{_google_data_path}/kvw/*.kvw
%dir %{_google_data_path}/lang
%{_google_data_path}/lang/*.qm
%dir %{_google_data_path}/res
%{_google_data_path}/res/*.png
%dir %{_google_data_path}/resources
%{_google_data_path}/resources/*.png
%{_google_data_path}/resources/*.jpg
%dir %{_google_data_path}/resources/de_DE.locale
%{_google_data_path}/resources/de_DE.locale/*
%dir %{_google_data_path}/resources/en_AU.locale
%{_google_data_path}/resources/en_AU.locale/*
%dir %{_google_data_path}/resources/en_CA.locale
%{_google_data_path}/resources/en_CA.locale/*
%dir %{_google_data_path}/resources/en_NZ.locale
%{_google_data_path}/resources/en_NZ.locale/*
%dir %{_google_data_path}/resources/en_UK.locale
%{_google_data_path}/resources/en_UK.locale/*
%dir %{_google_data_path}/resources/en_US.locale
%{_google_data_path}/resources/en_US.locale/*
%dir %{_google_data_path}/resources/es_ES.locale
%{_google_data_path}/resources/es_ES.locale/*
%dir %{_google_data_path}/resources/fr_FR.locale
%{_google_data_path}/resources/fr_FR.locale/*
%dir %{_google_data_path}/resources/it_IT.locale
%{_google_data_path}/resources/it_IT.locale/*
%dir %{_google_data_path}/xml
%{_google_data_path}/xml/*.xml
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
