Summary:	Applets you can use with AfterStep and compatible window managers.
Name:		AfterStep-APPS
Version:	990329
Release:	2
Copyright:	GPL
Group:		X11/Applications
Source0:	http://www.tigr.net/afterstep/as-apps/download/as-apps-%{version}.tar
Patch0:		AfterStep-APPS-1.5beta1-glibc.patch
Patch1:		ascp-paths.patch
Patch2:		as-apps-compile.patch
Patch3:		aterm-utmp.patch
Patch4:		xiterm-utmp.patch
Prereq:		/sbin/ldconfig
Requires:	/usr/sbin/utempter
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_prefix	/usr/X11R6
%define		_mandir	/usr/X11R6/man

%description
What's a cool window manager without some cool applets?
Well... it's still cool, but these applets which can
be used in the Wharf module for AfterStep or Window
Maker can add both spice and productivity to your
preferred window manager, such as a handy clock and
information about system resources.

If you've installed the AfterStep packages, you
should also install these packages. Enjoy! 

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
	    make Makefiles CXXDEBUGFLAGS="$RPM_OPT_FLAGS" \
	    	CDEBUGFLAGS="$RPM_OPT_FLAGS"
	    make MANDIR=%{_mandir}/man1 \
		BINDIR=%{_bindir} \
		SHLIBDIR=%{_libdir} \
		CXXDEBUGFLAGS="$RPM_OPT_FLAGS" \
		CDEBUGFLAGS="$RPM_OPT_FLAGS"
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
	    make CXXDEBUGFLAGS="$RPM_OPT_FLAGS" \
	    	CDEBUGFLAGS="$RPM_OPT_FLAGS"
	    ;;
	asclock*)
	    CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} << EOF
classic

EOF
             make CFLAGS="$RPM_OPT_FLAGS"
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
strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/afterstep/*
%{_mandir}/man1/*
