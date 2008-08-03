
Name:           kplayer
Epoch:	        1
Version:        0.6.2
Release:        4%{?dist}
Summary:        A KDE media player based on MPlayer

Group:          Applications/Multimedia
License:        GPL
URL:            http://kplayer.sourceforge.net/
Source0:	http://osdn.dl.sourceforge.net/sourceforge/kplayer/kplayer-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  kdelibs-devel

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
%setup -q

[ ! -f configure ] && \
make -f admin/Makefile.common


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

%configure \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-debug --disable-warnings \
  --disable-dependancy-tracking --disable-final

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

## File lists
# locale's
%find_lang %{name} || touch %{name}.lang
# HTML (1.0)
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    echo "%lang($lang) $HTML_DIR/$lang/*" >> %{name}.lang
    # replace absolute symlinks with relative ones
    pushd $lang_dir
      for i in *; do
        [ -d $i -a -L $i/common ] && rm -f $i/common && ln -sf ../common $i/common
      done
    popd
  fi
done
fi


%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/kde/*.desktop ||:


%clean
rm -rf $RPM_BUILD_ROOT


%post
for icon_theme in hicolor locolor ; do
  touch --no-create %{_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database -q %{_datadir}/applications 2>/dev/null || :

%postun
for icon_theme in hicolor locolor ; do
  touch --no-create %{_datadir}/icons/${icon_theme} 2> /dev/null ||:
  gtk-update-icon-cache -q %{_datadir}/icons/${icon_theme} 2> /dev/null ||:
done
update-desktop-database -q %{_datadir}/applications 2>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog COPYING README TODO
%{_bindir}/kplayer
%{_datadir}/applications/kde/*kplayer.desktop
%{_datadir}/apps/kplayer/
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/icons/locolor/*/*/*
%{_datadir}/services/*kplayer*.desktop
%{_libdir}/kde3/libkplayerpart.*


%changelog
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
