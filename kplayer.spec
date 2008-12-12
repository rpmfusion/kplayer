%define cvsversion 20081211cvs

Name:           kplayer
Epoch:          1
Version:        0.7.0
Release:        1.%cvsversion%{?dist}
Summary:        A media player based on MPlayer
Group:          Applications/Multimedia
License:        GPLv3+ and GFDL
URL:            http://kplayer.sourceforge.net/
Source0:        %{name}-%{version}-%cvsversion.tar.bz2
Source1:        %{name}-snapshot.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
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
%setup -q -n %{name}

%{cmake_kde4} -DCMAKE_SKIP_RPATH:BOOL=ON .


%build
make %{?_smp_mflags} VERBOSE=1 

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} 

## File lists
# locale's
%find_lang %{name} || touch %{name}.lang
# HTML (1.0)
HTML_DIR=$(kde4-config --expandvars --install html)
if [ -d %{buildroot}$HTML_DIR ]; then
for lang_dir in %{buildroot}$HTML_DIR/* ; do
  if [ -d $lang_dir ]; then
    lang=$(basename $lang_dir)
    # Install HTML docs in the correct location and
    mv $lang_dir $lang_dir.TMP
    mkdir $lang_dir
    mv $lang_dir.TMP $lang_dir/%{name}
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

# Install servicemenus in the correct location:
mkdir -p %{buildroot}%{_datadir}/kde4/services/ServiceMenus/
mv %{buildroot}%{_datadir}/kde4/apps/konqueror/servicemenus/* \
   %{buildroot}%{_datadir}/kde4/services/ServiceMenus/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/kde4/*.desktop ||:


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor 2> /dev/null ||:
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
update-desktop-database -q %{_datadir}/applications 2>/dev/null || :


%postun
touch --no-create %{_datadir}/icons/hicolor 2> /dev/null ||:
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
update-desktop-database -q %{_datadir}/applications 2>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog COPYING* README TODO
%{_bindir}/%{name}
%{_datadir}/applications/kde4/*%{name}.desktop
%{_datadir}/kde4/apps/%{name}/
%{_datadir}/kde4/services/*%{name}*.desktop
%{_datadir}/kde4/services/ServiceMenus/
%{_datadir}/icons/hicolor/*/*/*
%{_libdir}/kde4/lib%{name}part.*


%changelog
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
