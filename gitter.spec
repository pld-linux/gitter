Summary:	Instant messaging and chat room system for developers and users of GitHub repositories
Name:		gitter
Version:	2.4.0
Release:	0.4
License:	unknown
Group:		X11/Applications/Networking
Source0:	https://update.gitter.im/linux64/%{name}_%{version}_amd64.deb
# NoSource0-md5:	8bcf9ce074a7e191cf3070724dc7e525
NoSource:	0
Patch0:		desktop.patch
URL:		https://gitter.im/
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
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

%patch0 -p1

%build
# chrome official rpm just add libudev.so.0 -> libudev.so.1 symlink, so we use similar hack here
if [ ! -f Gitter.patched ] && grep -qE "libudev\.so\.0" Gitter; then
	%{__sed} -i -e 's#libudev\.so\.0#libudev.so.1#g' Gitter
	touch Gitter.patched
else
	echo >&2 "Hack no longer needed? No longer linked with libudev.so.0?"
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_desktopdir},%{_pixmapsdir}}

cp -a locales $RPM_BUILD_ROOT%{_appdir}
install -p Gitter $RPM_BUILD_ROOT%{_appdir}
install -p libffmpegsumo.so $RPM_BUILD_ROOT%{_appdir}
cp -p *.dat *.pak $RPM_BUILD_ROOT%{_appdir}
ln -s %{_appdir}/Gitter $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -p logo.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
cp -p gitter.desktop $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gitter
%{_desktopdir}/gitter.desktop
%{_pixmapsdir}/gitter.png
%dir %{_appdir}
%{_appdir}/locales
%{_appdir}/icudtl.dat
%{_appdir}/nw.pak
%attr(755,root,root) %{_appdir}/Gitter
%attr(755,root,root) %{_appdir}/libffmpegsumo.so
