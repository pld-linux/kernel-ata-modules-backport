#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		rel	0.rc8.1
%define		pname	kernel-ata-modules-backport
Summary:	ATA modules backport
Summary(pl.UTF-8):	Backportowane sterowniki ATA
Name:		%{pname}%{_alt_kernel}
Version:	2.6.31
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://pld.atwa.us/~shadzik/%{pname}/%{pname}-%{version}-rc8.tar.gz
# Source0-md5:	d5c25d1ab772bbb236e409f4a0f8caa0
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
These are backported ATA modules from linux %{version}.

%description -l pl.UTF-8
W tej paczce znajdują się zbackportowane sterowniki ATA z wersji
linuksa %{version}.

%prep
%setup -q -n %{pname}-%{version}-rc8
%define		modules		%(ls *.c |sed -e 's/\.c//')

%build
%build_kernel_modules -m %{modules}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/ata/
install -d $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}
for module in $(ls -1 *.ko); do
	modname=$(ls $module |sed -e 's/\.ko//')
	rm -f *.ko.*
	install $module $modname-current.ko
	gzip $modname-current.ko
	install $modname-current.ko.gz $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/ata/
	echo "blacklist $modname" >> $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
	echo "alias $modname $modname-current" >> $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/ata/*.ko*
