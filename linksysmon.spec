Summary:	A tool for monitoring Linksys BEFSR41 and BEFSR11 firewalls
Name:		linksysmon
Version:	1.1.4
Release:	6
License:	GPL or Artistic
Group:		System/Servers
URL:		https://woogie.net/projects/linksysmon/
Source0:	http://woogie.net/projects/linksysmon/attachment/wiki/WikiStart/%{name}-%{version}.tar.bz2
Source1:	linksysmon.init.bz2
Source2:	linksysmon.sysconfig.bz2
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	perl-devel
Requires:	net-snmp
Requires:	net-snmp-utils
Requires:	net-snmp-trapd
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
linksysmon is a tool for monitoring Linksys BEFSR41 and BEFSR11
firewalls under Linux and other Unix-like operating systems (I
specify Linux because that is what I used to develop it, and the
only one I know for sure works). It accepts log mesages from the
Linksys, and logs the messages to /var/log/linksys.log. It handles
the standard activity logs, as well as the "secret" extended
logging, and can handle logs from multiple firewalls. When using
extended logging, it can detect external IP address changes (if
you are using either DHCP or PPPOE) and can call an external
program to process the change.

%prep

%setup -q -n %{name}-%{version}

bzcat %{SOURCE1} > linksysmon.init
bzcat %{SOURCE2} > linksysmon.sysconfig

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor


%make
make test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}

%makeinstall_std

install -m0755 linksysmon.init %{buildroot}%{_initrddir}/linksysmon
install -m0644 linksysmon.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/linksysmon

install -m0644 etc/linksysmon.conf %{buildroot}%{_sysconfdir}/linksysmon.conf
install -m0755 etc/cron.daily/linksysmon-report %{buildroot}%{_sysconfdir}/cron.daily/linksysmon-report

install -m0755 usr/sbin/linksysmon %{buildroot}%{_sbindir}/
install -m0755 usr/sbin/linksysmon-ez-ipupdate %{buildroot}%{_sbindir}/
install -m0755 usr/sbin/linksysmon-ipchange %{buildroot}%{_sbindir}/
install -m0755 usr/sbin/linksysmon-report %{buildroot}%{_sbindir}/
install -m0755 usr/sbin/linksysmon-watch %{buildroot}%{_sbindir}/

# install log rotation stuff
cat > %{buildroot}%{_sysconfdir}/logrotate.d/linksysmon << EOF
/var/log/linksys.log {
    missingok
    postrotate
	%{_initrddir}/linksysmon restart > /dev/null || /bin/true
    endscript
}
EOF

%post
%_post_service linksysmon

%preun
%_preun_service linksysmon

%clean 
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS CHANGELOG COPYING INSTALL README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/linksysmon.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/linksysmon
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/linksysmon
%attr(0755,root,root) %{_sysconfdir}/cron.daily/linksysmon-report
%attr(0755,root,root) %{_initrddir}/linksysmon
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{perl_vendorlib}/linksysmon.pm




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-5mdv2011.0
+ Revision: 620241
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.1.4-4mdv2010.0
+ Revision: 429853
- rebuild

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 1.1.4-3mdv2009.0
+ Revision: 250812
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.1.4-1mdv2008.1
+ Revision: 136572
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Mar 02 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-1mdv2007.0
+ Revision: 131191
- Import linksysmon

* Wed Feb 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-1mdk
- initial Mandriva package

