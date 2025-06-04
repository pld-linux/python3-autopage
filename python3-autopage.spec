# Conditional build:
%bcond_without	tests	# unit tests

%define		module	autopage
Summary:	A library to provide automatic paging for console output
Name:		python3-%{module}
Version:	0.5.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/autopage/
Source0:	https://files.pythonhosted.org/packages/source/a/autopage/%{module}-%{version}.tar.gz
# Source0-md5:	57936e4a9d379fe4a60eb617d8cdce33
URL:		https://pypi.org/project/autopage/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Autopage is a Python library to automatically display terminal output
from a program in a pager (like less) whenever you need it, and never
when you don't. And it only takes one line of code.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" autopage/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/py.typed
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
