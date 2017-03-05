%define module evdi 
%define version 1.3.52 


Name: displaylink-driver
Version: %{version}
Release: 1%{?dist}
Summary: Driver for displaylink adaptors and displays

License: Complicated
Source0: displaylink-driver-%{version}.run
Source1: dlm.service
Source2: 99-displaylink.rules
Source3: suspend.sh
Source4: dkms.conf
Source5: udev.sh

Nosource: 0

Requires: dkms >= 1.00
Requires: bash
Requires: kernel-headers
Requires: kernel-devel


%description
The Ubuntu Displaylink driver repackaged for Fedora

%prep
rm -rf %{_builddir}/%{name}-%{version}
mkdir %{_builddir}/%{name}-%{version}
%{SOURCE0} --noexec --keep --target %{_builddir}/%{name}-%{version}



%install 
mkdir -p %{buildroot}/%{_usr}/src/%{module}-%{version}/
cd %{buildroot}/%{_usr}/src/%{module}-%{version}/
tar xzf %{_builddir}/%{name}-%{version}/%{module}-%{version}-src.tar.gz
install %{SOURCE4} %{buildroot}/%{_usr}/src/evdi-%{version}/

mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system/
install %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system/

mkdir -p  %{buildroot}/%{_sysconfdir}/udev/rules.d/
install -m 6440 %{SOURCE2} %{buildroot}/%{_sysconfdir}/udev/rules.d/

mkdir -p %{buildroot}/%{_usr}/lib/systemd/system-sleep/
install %{SOURCE3} %{buildroot}/%{_usr}/lib/systemd/system-sleep/

mkdir -p %{buildroot}/opt/displaylink
cp %{_builddir}/%{name}-%{version}/x64-ubuntu-1604/* %{buildroot}/opt/displaylink
cp %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/opt/displaylink
cp %{_builddir}/%{name}-%{version}/*.spkg %{buildroot}/opt/displaylink

ln -sf ./libusb-1.0.so.0.1.0 %{buildroot}/opt/displaylink/libusb-1.0.so.0
ln -sf ./libusb-1.0.so.0.1.0 %{buildroot}/opt/displaylink/libusb-1.0.so

install -m 7550  %{SOURCE5}  %{buildroot}/opt/displaylink

%files
%{_usr}/lib/systemd/system-sleep/*
%{_usr}/lib/systemd/system/*
/opt/displaylink
%{_sysconfdir}/udev/rules.d/*
%{_usr}/src/evdi-%{version}




%post
occurrences=/usr/sbin/dkms status | grep "%{module}" | grep "%{version}" | wc -l
if [ ! occurrences > 0 ];
then
    /usr/sbin/dkms add -m %{module} -v %{version} --rpm_safe_upgrade
fi
/usr/sbin/dkms build -m %{module} -v %{version}
/usr/sbin/dkms install -m %{module} -v %{version}
udevadm control -R
udevadm trigger
exit 0


%preun
/usr/sbin/dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
udevadm control -R
udevadm trigger
exit 0


%changelog
