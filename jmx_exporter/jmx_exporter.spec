%global debug_package %{nil}

Name:    jmx_exporter
Version: 0.17.2
Release: 1%{?dist}
BuildArch: noarch
Summary: Prometheus exporter for mBeans scrape and expose.
License: ASL 2.0
URL:     https://github.com/prometheus/%{name}

Source0: https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/%{version}/jmx_prometheus_javaagent-%{version}.jar 
Source1: %{name}.service
Source2: %{name}.default

Requires: java
%{?systemd_requires}
%if 0%{?fedora} >= 19
BuildRequires: systemd-rpm-macros
%endif

%description

A Collector that can configurable scrape and expose mBeans of a JMX target. It meant to be run as a Java Agent, exposing an HTTP server and scraping the local JVM.

%prep

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 644 %{SOURCE0} %{buildroot}%{_datarootdir}/prometheus/%{name}/%{name}.jar
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_datarootdir}/prometheus/%{name}/%{name}.jar
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
