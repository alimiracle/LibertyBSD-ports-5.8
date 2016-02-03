# $OpenBSD: Makefile.inc,v 1.32 2015/06/26 18:08:39 ajacoutot Exp $

SHARED_ONLY=		Yes

CATEGORIES +=		sysutils

# GPLv2+
PERMIT_PACKAGE_CDROM?=	Yes

.if ! defined(WANTLIB)
MODULES +=		devel/gettext

LIB_DEPENDS +=		x11/gtk+2

WANTLIB += X11 Xcomposite Xcursor Xdamage Xext Xfixes Xi Xinerama
WANTLIB += Xrandr Xrender atk-1.0 cairo fontconfig freetype gdk-x11-2.0
WANTLIB += gdk_pixbuf-2.0 gio-2.0 glib-2.0 gobject-2.0 gtk-x11-2.0
WANTLIB += m pango-1.0 pangocairo-1.0 pangoft2-1.0 pthread z
.endif

.if defined(EXTRA_WANTLIB)
WANTLIB +=	${EXTRA_WANTLIB}
.endif

BUILD_DEPENDS +=	sysutils/gkrellm/gkrellm,-client
RUN_DEPENDS +=		sysutils/gkrellm/gkrellm,-client

NO_TEST=		Yes
USE_GMAKE=		Yes

PLUGINDIR=	${PREFIX}/lib/gkrellm2/plugins

do-install:
	${INSTALL_DATA_DIR} ${PLUGINDIR}
	${INSTALL_DATA} ${PLUGIN} ${PLUGINDIR}