Summary:	Applets you can use with AfterStep and compatible window managers
Summary(pl):	Aplety, których mo¿esz u¿ywaæ z AfterStepem oraz innymi zarz±dcami okien, które s± z nim kompatybilne
Name:		AfterStep-APPS
Version:	991125
Release:	4
License:	GPL
Group:		X11/Window Managers/Tools
Source0:	http://www.tigr.net/afterstep/download/as-apps-%{version}.tar
Patch0:		%{name}-1.5beta1-glibc.patch
Patch1:		xiterm-utmp.patch
Patch2:		as-apps-miniCHESS-change_install_dirs.patch
Patch3:		as-apps-ascd-configure_and_install_bugfix.patch
#Patch4:        ascp-paths.patch
#Patch5:        aterm-utemp.patch
URL:		http://www.tigr.net/afterstep/
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
%patch2 -p1
%patch3 -p1
#patch4
#patch5

%build
for package in `ls` ; do
    cd $package
    case $package in
	ascd-* )
	    ./configure << EOF
/dev/cdrom
%{_bindir}
%{_mandir}/man1
%{_datadir}/afterstep/AScd
2
EOF
	    xmkmf
	    make Makefiles CXXDEBUGFLAGS="%{rpmcflags}" \
	    	CDEBUGFLAGS="%{rpmcflags}"
	    make MANDIR=%{_mandir}/man1 \
		BINDIR=%{_bindir} \
		SHLIBDIR=%{_libdir} \
		CXXDEBUGFLAGS="%{rpmcflags}" \
		CDEBUGFLAGS="%{rpmcflags}"
	    ;;

	aterm* )
	    ## This program is provided by aterm rpm package.

	    # configure2_13 --enable-utmp
	    # make
	    ;;
	asclock*)
	    CFLAGS="%{rpmcflags}" ./configure --prefix=%{_prefix} << EOF
classic

EOF
             make CFLAGS="%{rpmcflags}"
	     ;;

	ascp-* )

	    ## There is strange problem with this program.
	    ## The ./configure script tries to run /usr/local/bin/gtk-config
	    ## program. In PLD it should be %{_bindir}/gtk-config.
	    ##
	    ##    --with-gtk-prefix
	    ##    --with-gtk-exec-prefix
	    ## or --disable-gtktest
	    ## not help here. I don't now why.

# export LD_LIBRARY_PATH=%{_prefix}/
	    # configure2_13 \
	    #	--enable-i18n \
	    #   --x-includes=%{_includedir} \
	    #	--x-libraries=%{_libdir} \
	    #   --disable-gtktest
# --with-gtk-prefix=%{_prefix} \
            #	--with-gtk-exec-prefix=%{_bindir}
	    # make
	    ;;

	asfatm-* )
	    ## <sensors/sensors.h> is needed to compile this program.
	    ## I don't have it.

	    # cd asfatm
	    # make
	    ;;

	asppp-* )
	    ## xpminit.c:7: dial.xpm: No such file or directory

	    # configure2_13
	    # make
	    ;;

	miniCHESS-* )
	    #chess.c: In function `mouseGame':
	    #chess.c:1667: `fd_set' undeclared (first use in this function)
	    #chess.c:1667: (Each undeclared identifier is reported only once
	    #chess.c:1667: for each function it appears in.)
	    #chess.c:1667: parse error before `fdset'
	    #chess.c:1687: `fdset' undeclared (first use in this function)
	    #chess.c: In function `main':
	    #chess.c:1975: warning: return type of `main' is not `int'

	    #make
	    ;;

	xiterm* )
	    ## You can try to build this program,
	    ## if only you have got utempter-devel.

	    # cough cough, hack hack -- ewt
	    # configure2_13 \
	    #	--enable-xpm-background \
	    #	--enable-utmp \
	    #	--enable-wtmp 	\
	    #	--enable-menubar \
	    #	--enable-next-scroll
	    #    xmkmf
	    #    make Makefiles
	    #    cd src
	    #    sed -e "s/EXTRA_LIBRARIES =/EXTRA_LIBRARIES = -lutempter/" \
	    #       Makefile > Makefile.foo
	    #    sed -e "s/-lsocket //" Makefile.foo > Makefile
	    #    make CXXDEBUGFLAGS="%{rpmcflags}" \
	    #    	CDEBUGFLAGS="%{rpmcflags}"
	    ;;

	Tasks-*)
	    ## I think this program is not finished yet.
	    ## There is Makefile.in but I can't find anything to
	    ## create Makefile (there is no ./configure or configure.in)
	    ## I think that `mv Makefile.in Makefile' will be enough.
	    ## I will try this later.
	    ;;
	xfascd-*)
	    ## I'll try to build this program later.
	    ;;

        asmount* | asDrinks* | asbutton* | asdm* | aspbm* | aspostit* \
        | ascdc-* | astuner* | ASFiles* | as[R-W]* | asfaces* | asmon* \
        | astrash* | asxmcd* | asampmenu* | randbg-*)
	    ## We don't compile these
	    ;;

	*)
	    #just about every other thing supports autoconf

	    %configure2_13
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

	ascd-* )
	    make install install.man \
	        AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
		AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
		MANDIR=%{_mandir}/man1 \
		BINDIR=%{_bindir} \
		SHLIBDIR=%{_libdir} \
		DESTDIR=$RPM_BUILD_ROOT
	    ;;

	aterm*)
	    ## This program is provided by aterm.rpm package.

	    # make install \
	    #    AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	    #	AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	    #	DESTDIR=$RPM_BUILD_ROOT
	    ;;

	xiterm*)
	    ## You can try to install this program,
            ## if only you have got utempter-devel.
	    ## Don't forget build it first.


	    # make install install.man \
	    #   AFTER_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	    #	AFTER_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	    #	MANDIR=%{_mandir}/man1 \
	    #	BINDIR=%{_bindir} \
	    #	SHLIBDIR=%{_libdir} \
	    #	DESTDIR=$RPM_BUILD_ROOT
	    ;;

	asfatm-*)
	    ## We don't install this.
	    ;;

        ascp-*)
    	    ## We do not install this. (If you want to know why check
	    ## the build section above).

	    # make install \
	    #   ASCP_BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	    #	ASCP_MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	    #	prefx=$RPM_BUILD_ROOT \
	    #	DESTDIR=$RPM_BUILD_ROOT
	    ;;

	asppp-* | miniCHESS-* | Tasks-* | xfascd-*)
	    ## There were problems with these programs in build section.
	    ## We can not install it.
	    ;;
        asmount* | asDrinks* | asbutton* | asdm* | aspbm* | aspostit* \
        | ascdc-* | astuner* | ASFiles* | as[R-W]* | asfaces* | asmon* \
        | astrash* | asxmcd* | asampmenu* | randbg-*)
	    ## We don't install these
	    ;;

	*)
	    echo
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%{_datadir}/afterstep/*
%{_mandir}/man1/*
%{_libdir}/*
