Summary:	Lexmark printer management commands
Name:		lxcontrol
Version:	1.3 
Release:	%mkrel 1
License:	GPL
Group:		System/Configuration/Printing
Source:		http://www.powerup.com.au/~pbwest/lexmark/lexmark.html/lxcontrol.tar.bz2
Source1:	http://209.233.17.85/lexmark/lm1100maint.tar.bz2
Source2:	http://bimbo.fjfi.cvut.cz/~paluch/l7kdriver/changecartridge
Source3:	README.changecartridge
Source4:	README.Lexmark-Maintenance
Source5:	lx.control.sh
Patch0:		lxcontrol-lx.control-cups.patch
Requires:	cups
Conflicts:	printer-utils-2006 printer-utils-2007
Conflicts:	printer-filters-2006 printer-filters-2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Tools for show and hide catridges, and align and clean heads in a Lexmark
printer. Used with Lexmark 5xxx, 7xxx and 11xx, possible with others.

%prep

%setup -q -n %{name}
%setup -q -n %{name} -a 1 -T -D
cp %{SOURCE2} changecartridge
mv README.Lexmark README.Lexmark5xxx_7xxx
mv lm1100maint/README README.Lexmark1xxx
cp %{SOURCE3} .
cp %{SOURCE4} .
%patch0 -p1

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/lxcontrol
install -d %{buildroot}%{_datadir}/lm1100maint
install -d %{buildroot}%{_datadir}/applications

# Lexmark printer maintenance
# Program and data files
install -m 755 lx.control %{buildroot}%{_bindir}/
install -m 755 %{_sourcedir}/lx.control.sh %{buildroot}%{_bindir}/
install -m 755 lm1100maint/lm1100change %{buildroot}%{_bindir}/
install -m 755 lm1100maint/lm1100back %{buildroot}%{_bindir}/
install -m 755 changecartridge %{buildroot}%{_bindir}/
cp -f *.out %{buildroot}%{_datadir}/lxcontrol/
( cd %{buildroot}%{_bindir}
  ln -s lx.control headclean
  ln -s lx.control headalign
  ln -s lx.control showcartridges
  ln -s lx.control hidecartridges
  ln -s lx.control.sh headclean.sh
  ln -s lx.control.sh headalign.sh
  ln -s lx.control.sh showcartridges.sh
  ln -s lx.control.sh hidecartridges.sh
)
cp -f lm1100maint/lexmark* \
	%{buildroot}%{_datadir}/lm1100maint/

# XDG menu
install -d %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/mandriva-headalign.desktop << EOF
[Desktop Entry]
Name=Lexmark headalign
Comment=Lexmark Lexmark 5xxx, 7xxx and 11xx Head Aligner
Exec=%{_bindir}/headalign.sh
Icon=printmgr
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-headclean.desktop << EOF
[Desktop Entry]
Name=Lexmark headclean
Comment=Lexmark Lexmark 5xxx, 7xxx and 11xx Head Cleaner
Exec=%{_bindir}/headclean.sh
Icon=printmgr
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-hidecartridges.desktop << EOF
[Desktop Entry]
Name=Lexmark hidecartridges
Comment=Lexmark Lexmark 5xxx, 7xxx and 11xx Cartridges Hider
Exec=%{_bindir}/hidecartridges.sh
Icon=printmgr
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-showcartridges.desktop << EOF
[Desktop Entry]
Name=Lexmark showcartridges
Comment=Lexmark Lexmark 5xxx, 7xxx and 11xx Cartridges Viewer
Exec=%{_bindir}/showcartridges.sh
Icon=printmgr
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/*
%{_datadir}/lm1100maint
%{_datadir}/lxcontrol
%{_datadir}/applications/*
