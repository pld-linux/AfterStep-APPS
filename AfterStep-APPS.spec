Summary:	Applets you can use with AfterStep and compatible window managers
Summary(pl):	Aplety, których mo¿esz u¿ywaæ z AfterStepem oraz innymi zarz±dcami okien, które s± z nim kompatybilne
Name:		AfterStep-APPS
Version:	991125
Release:	3
License:	GPL
Group:		X11/Window Managers/Tools
Group(de):	X11/Fenstermanager/Werkzeuge
Group(pl):	X11/Zarz±dcy Okien/Narzêdzia
Source0:	http://www.tigr.net/afterstep/as-apps/download/as-apps-%{version}.tar
Patch0:		%{name}-1.5beta1-glibc.patch
Patch1:		ascp-paths.patch
Patch2:		as-apps-compile.patch
Patch3:		aterm-utmp.patch
Patch4:		xiterm-utmp.patch
Prereq:		/sbin/ldconfig
Requires:	/usr/sbin/utempter
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		/usr/X11R6/man

%description
What's a cool window manager without some cool applets? Well... it's
still cool, but these applets which can be used in the Wharf module
for AfterStep or Window Maker can add both spice and productivity to
your preferred window manager, such as a handy clock and information
about system resources.

If you've installed the AfterStep packages, you should also install
these packages. Enjoy!

%description -l pl
Czym jest fajny zarz±dca okien bez fajnych apletów? Có¿... jest nadal
fajnym zarz±dc± okien, ale aplety, które mog± byæ u¿ywane w module
Wharf AfterStepa lub Window Makera, mog³yby zwiêkszyæ efektywno¶æ i
efektowno¶æ twojego ulubionego zarz±dcy okien.

Je¿eli masz zainstalowanego AfterStepa to powiniene¶ zainstalowaæ
tak¿e ten pakiet. Mi³ej zabawy!

%prep
%setup -q -c
rm -f *.asc
for archive in *.tar.gz ; do
	tar xzf $archive
	rm -f $archive
done
%patch0 -p1
%patch1 -p1
%patch3 -p0
%patch4 -p1

%build
for package in `ls` ; do
    cd $package 
    case $package in
	ascd-* )
	    ./configure << EOF
1

1

EOF
	    patch -p2 -b --suffix .compile < %{PATCH2}
	    xmkmf
	    make Makefiles CXXDEBUGFLAGS="%{rpmcflags}" \
	    	CDEBUGFLAGS="%{rpmcflags}"
	    make MANDIR=%{_mandir}/man1 \
		BINDIR=%{_bindir} \
		SHLIBDIR=%{_libdir} \
		CXXDEBUGFLAGS="%{rpmcflags}" \
		CDEBUGFLAGS="%{rpmcflags}"
	    ;;
	
	asmount* | asDrinks* | asbutton* | asdm* | aspbm* | aspostit* | ascdc-* | astuner* | ASFiles* | as[R-W]* | asfaces* | asmon* | astrash* | asxmcd* )
	    # we don't compile these
	    ;;

	aterm*)
	    %configure --enable-utmp
	    make
	    ;;

	xiterm*)
	    # cough cough, hack hack -- ewt
	    %configure \
		--enable-xpm-background \
		--enable-utmp \
		--enable-wtmp \
		--enable-menubar \
		--enable-next-scroll
	    xmkmf
	    make Makefiles
	    cd src
	    sed -e "s/EXTRA_LIBRARIES =/EXTRA_LIBRARIES = -lutempter/" \
	       Makefile > Makefile.foo
	    sed -e "s/-lsocket //" Makefile.foo > Makefile
	    make CXXDEBUGFLAGS="%{rpmcflags}" \
	    	CDEBUGFLAGS="%{rpmcflags}"
	    ;;
	asclock*)
	    CFLAGS="%{rpmcflags}" ./configure --prefix=%{_prefix} << EOF
classic

EOF
             make CFLAGS="%{rpmcflags}"
	     ;;
	*)
	    #just about every other thing supports autoconf
	    %configure
	    make
	    ;;
    esac
    cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

for package in `ls` ; do
    cd $package 
    case $package in
	ascd-* | xiterm*)
	    make install install.man \
	        AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
		AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
		MANDIR=%{_mandir}/man1 \
		BINDIR=%{_bindir} \
		SHLIBDIR=%{_libdir} \
		DESTDIR=$RPM_BUILD_ROOT	
	    ;;

	asmount* | asDrinks* | asbutton* | asdm* | aspbm* | aspostit* | ascdc-* | astuner* | ASFiles* | as[R-W]* | asfaces* | asmon* | astrash* | asxmcd* )
	    # we don't install this
	    ;;

        ascp-* )
	    make install \
	        ASCP_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
		ASCP_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
		prefx=$RPM_BUILD_ROOT \
		DESTDIR=$RPM_BUILD_ROOT
	    ;;
	
	asppp* | aterm* )
	    make install \
	        AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
		AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
		DESTDIR=$RPM_BUILD_ROOT
	    ;;
	*)
	    make install install.man \
	        AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
		AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
		DESTDIR=$RPM_BUILD_ROOT
	    ;;
    esac
    cd ..
done
rm -f $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}/{sessreg,xpmroot,qplot}*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/afterstep/*
%{_mandir}/man1/*
