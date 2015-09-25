Summary:	Instant messaging and chat room system for developers and users of GitHub repositories
Name:		gitter
Version:	2.4.0
Release:	0.1
License:	unknown
Group:		X11/Applications/Networking
Source0:	https://update.gitter.im/linux64/%{name}_%{version}_amd64.deb
# NoSource0-md5:	8bcf9ce074a7e191cf3070724dc7e525
NoSource:	0
URL:		https://gitter.im/
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%define		_appdir	%{_libdir}/%{name}

%description
Gitter is built on top of GitHub and is tightly integrated with your
organisations, repositories, issues and activity.

%prep
%setup -qcT
%ifarch %{x8664}
SOURCE=%{S:0}
%endif

ar x $SOURCE
tar xf control.tar.gz && rm control.tar.gz
tar xf data.tar.gz && rm data.tar.gz

version=$(awk '/Version:/{print $2}' control)
test $version = %{version}

mv opt/Gitter/linux*/* .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir}}

cp -a locales $RPM_BUILD_ROOT%{_appdir}
install -p Gitter $RPM_BUILD_ROOT%{_appdir}
install -p libffmpegsumo.so $RPM_BUILD_ROOT%{_appdir}
cp -p *.dat *.pak $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/Gitter $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gitter
%dir %{_appdir}
%{_appdir}/locales
%{_appdir}/icudtl.dat
%{_appdir}/nw.pak
%attr(755,root,root) %{_appdir}/Gitter
%attr(755,root,root) %{_appdir}/libffmpegsumo.so
