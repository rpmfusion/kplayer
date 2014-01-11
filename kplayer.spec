%define cvsversion 20081211cvs

Name:           kplayer
Epoch:          1
Version:        0.7.0
Release:        10.%cvsversion%{?dist}
Summary:        A media player based on MPlayer
License:        GPLv3+ and GFDL
URL:            http://kplayer.sourceforge.net/
Source0:        %{name}-%{version}-%cvsversion.tar.bz2
Source1:        %{name}-snapshot.sh
# Fix DSO linking
Patch0:         %{name}-linking.patch
# Match the .desktop file to freedesktop standards
Patch1:         %{name}-desktop-fix.patch
# Fix docdir install path
Patch2:         %{name}-docdir.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs4-devel

Requires:       mplayer
#Requires(hint): libdvdcss

%description
KPlayer is a KDE media player based on MPlayer, www.mplayerhq.hu.
With KPlayer you can easily play a wide variety of video and audio
files and streams using a rich and friendly interface compliant with
KDE standards.  Features include
- video, audio and subtitle playback from file, URL, DVD, VCD,
  audio CD, TV, DVB, etc., as well as KDE I/O Slaves;
- volume, contrast, brightness, hue and saturation controls;
- zooming, full screen and fixed aspect options;
- status and progress display and seeking;
- playlist;
- configuration dialog and file specific options;
- KPart for integration with Konqueror, KMLDonkey, etc.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .linking
%patch1 -p1 -b .fixdesktop
%patch2 -p1 -b .docdir

%{cmake_kde4} .

# Fix documentation build
sed -i 's|V4.1.2|V4.2|' doc/*/index.docbook

%build
make %{?_smp_mflags} 

%install
make install/fast DESTDIR=%{buildroot} 

## File lists
# locale's
%find_lang %{name} --with-kde 

# Install servicemenus in the correct location:
mkdir -p %{buildroot}%{_kde4_datadir}/kde4/services/ServiceMenus/
mv %{buildroot}%{_kde4_appsdir}/konqueror/servicemenus/* \
   %{buildroot}%{_kde4_datadir}/kde4/services/ServiceMenus/


%check
desktop-file-validate \
   %{buildroot}%{_kde4_datadir}/applications/kde4/kplayer.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog COPYING* README TODO
%{_kde4_bindir}/%{name}
%{_kde4_datadir}/applications/kde4/*%{name}.desktop
%{_kde4_appsdir}/%{name}/
%{_kde4_datadir}/kde4/services/*%{name}*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/kde4/lib%{name}part.*


%changelog
* Sat Jan 11 2014 Rex Dieter <rdieter@fedoraproject.org> 1:0.7.0-10.20081211cvs
- respin desktop-fix.patch so kbuildsycoca4 is happy too
- docdir.patch
- .spec cleanup

* Mon May 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:0.7.0-9.20081211cvs
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:0.7.0-8.20081211cvs
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:0.7.0-7.20081211cvs
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:0.7.0-6.20081211cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 03 2011 Orcan Ogetbil < orcanbahri [AT] yahoo [DOT] com> - 1:0.7.0-5.20081211cvs
- Fixed the documentation build

* Mon Jan 03 2011 Orcan Ogetbil < orcanbahri [AT] yahoo [DOT] com> - 1:0.7.0-4.20081211cvs
- Rebuild to workaround bug#1588

* Sun Aug 15 2010 Orcan Ogetbil < orcanbahri [AT] yahoo [DOT] com> - 1:0.7.0-3.20081211cvs
- Fix mimetypes in the .desktop file (RFBZ#1195)
- Switch to modern scriptlets
- Use kde4 macros
- Fix DSO linking

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.7.0-2.20081211cvs
- rebuild for new F11 features

* Fri Dec 12 2008 Orcan Ogetbil < orcanbahri [AT] yahoo [DOT] com> - 1:0.7.0-1.20081211cvs
- kplayer-0.7.0
- License is GPLv3+ and GFDL

* Thu Sep 04 2008 Rex Dieter <rdieter@fedoraproject.org> - 1:0.6.3-2
- kplayer-0.6.3
- License: GPLv3

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.6.2-4
- rebuild

* Fri Nov 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1:0.6.2-3
- revert to kplayer-0.6.2 (+Epoch), newer releases are gplv3, which
  is incompatible with qt's gplv2 license.

* Fri Oct 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.6.3-1
- kplayer-0.6.3

* Thu May 24 2007 Rex Dieter <rexdieter[AT]users.sf.net> 0.6.2-2
- kplayer-0.6.2

* Sun Mar 04 2007 Rex Dieter <rexdieter[AT]users.sf.net> 0.6.1-2
- kplayer-0.6.1

* Wed Jan 24 2007 Rex Dieter <rexdieter[AT]users.sf.net> 0.6-1
- kplayer-0.6 (#1382)

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.3-5
- respin

* Wed May 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.3-4
- disable kfile_kplayer (#933)
- simplify fix for kdelibs conflicts

* Thu Mar 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.3-3
- drop -desktop patch
- cleanup %%lang'ification
- cleanup BR's.
- .desktop: --add-category="AudioVideo"

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sat Jun  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.3-0.lvn.2
- Fix kdelibs conflict avoidance on FC4 (#459).
- Update desktop database and GTK icon cache after (un)installation.
- Reduce dir ownership bloat.

* Mon Jan 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.3-0.lvn.1
- Update to 0.5.3.

* Tue Oct  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.2-0.lvn.1
- Update to 0.5.2.
- Disable dependency tracking to speed up the build.

* Mon Jul  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.1-0.lvn.1
- Update to 0.5.1.

* Sun Jul  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.0-0.lvn.2
- Fix build on Qt 3.1.

* Sat Jul  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.5.0-0.lvn.1
- Update to 0.5.0.
- s/fedora/livna/ in desktop entry.

* Sun Nov  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.lvn.1
- Update to 0.4.0.

* Mon Oct 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.1-0.fdr.1
- Update to 0.3.1.

* Thu Jul 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.0-0.fdr.1
- First build.
