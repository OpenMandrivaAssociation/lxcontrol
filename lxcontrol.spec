Summary:	Lexmark printer management commands
Name:		lxcontrol
Version:	1.3 
Release:	12
License:	GPL
Group:		System/Printing
URL:		http://www.lxde.org/
Source:		http://www.powerup.com.au/~pbwest/lexmark/lexmark.html/lxcontrol.tar.bz2
Source1:	http://209.233.17.85/lexmark/lm1100maint.tar.bz2
Source2:	http://bimbo.fjfi.cvut.cz/~paluch/l7kdriver/changecartridge
Source3:	README.changecartridge
Source4:	README.Lexmark-Maintenance
Source5:	lx.control.sh
Patch0:		lxcontrol-lx.control-cups.patch
Requires:	cups
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007


%description
Tools for show and hide catridges, and align and clean heads in a Lexmark
printer. Used with Lexmark 5xxx, 7xxx and 11xx, possible with others.


%files
%{_bindir}/*
%{_datadir}/lm1100maint
%{_datadir}/lxcontrol
%{_datadir}/applications/*


#----------------------------------------------------------------------


%prep

%setup -q -n %{name}
%setup -q -n %{name} -a 1 -T -D
%apply_patches

cp %{SOURCE2} changecartridge
mv README.Lexmark README.Lexmark5xxx_7xxx
mv lm1100maint/README README.Lexmark1xxx
cp %{SOURCE3} .
cp %{SOURCE4} .

%build
# nothing to do here

%install
install -dm 0755 %{buildroot}%{_bindir}
install -dm 0755 %{buildroot}%{_datadir}/lxcontrol
install -dm 0755 %{buildroot}%{_datadir}/lm1100maint
install -dm 0755 %{buildroot}%{_datadir}/applications

# Lexmark printer maintenance
# Program and data files
install -pm 0755 lx.control %{buildroot}%{_bindir}/
install -pm 0755 %{_sourcedir}/lx.control.sh %{buildroot}%{_bindir}/
install -pm 0755 lm1100maint/lm1100change %{buildroot}%{_bindir}/
install -pm 0755 lm1100maint/lm1100back %{buildroot}%{_bindir}/
install -pm 0755 changecartridge %{buildroot}%{_bindir}/
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
install -dm 0755 %{buildroot}%{_datadir}/applications

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

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3-10mdv2011.0
+ Revision: 666110
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3-9mdv2011.0
+ Revision: 606436
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3-8mdv2010.1
+ Revision: 521149
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.3-7mdv2010.0
+ Revision: 426020
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.3-6mdv2009.0
+ Revision: 223135
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.3-5mdv2008.1
+ Revision: 152888
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.3-4mdv2008.1
+ Revision: 152887
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3-3mdv2008.0
+ Revision: 75343
- fix deps (pixel)

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3-2mdv2008.0
+ Revision: 64163
- use the new System/Printing RPM GROUP

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.3-1mdv2008.0
+ Revision: 61614
- Import lxcontrol



* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.4.3-1mdv2008.0
- initial Mandriva package

* Thu May 27 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-27 11:18:35 (61474)
- Fix translations.

* Thu May 27 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-27 10:47:52 (61470)
- Fix buildroot.

* Thu May 27 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-27 10:45:24 (61469)
- Updated .desktop Comment's so that they inform the printer the util is
  built for.

* Thu May 27 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-27 10:39:29 (61468)
- Added graphical interface to the tools. Closes: #12216

* Sat May 08 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-08 19:14:24 (59811)
- Put back %%{_bindir} to %%files section.

* Fri May 07 2004 Wanderlei Antonio Cavassin <cavassin@conectiva.com.br>
+ 2004-05-07 21:49:31 (59766)
- Removed old menu support

* Mon Mar 01 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-03-01 09:24:44 (50559)
- Added patch lx.control-cups, which makes lx.control correctly see
  our cups' lpc command.
- Removed the Requires for printer-utils
- Added Requires to cups, since it's the only required package to this
  one works.

* Thu Aug 29 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
+ 2002-08-29 18:19:33 (8651)
- Imported package from 8.0.
