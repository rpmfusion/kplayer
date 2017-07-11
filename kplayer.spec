Name:           kplayer
Epoch:          1
Version:        0.7.2
Release:        1%{?dist}
Summary:        A media player based on MPlayer
License:        GPLv3+ and GFDL
URL:            https://github.com/KDE/kplayer
Source0:        %url/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Match the .desktop file to freedesktop standards
Patch0:         %{name}-desktop-fix.patch

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
%autosetup -p1

# Fix documentation build
sed -i 's|V4.1.2|V4.2|' doc/*/index.docbook

%build
%{cmake_kde4} .
%make_build 

%install
make install/fast DESTDIR=%{buildroot} 

## File lists
# locale's
%find_lang %{name} --with-kde 

%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/kplayer.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS BUGS ChangeLog README TODO
%license COPYING*
%{_kde4_bindir}/%{name}
%{_kde4_datadir}/applications/kde4/*%{name}.desktop
%{_kde4_appsdir}/%{name}/
%{_kde4_datadir}/kde4/services/*%{name}*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/kde4/lib%{name}part.*


%changelog
* Tue Jul 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:0.7.2-1
- kplayer-0.7.2

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1:0.7.0-12.20081211cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1:0.7.0-11.20081211cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

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
