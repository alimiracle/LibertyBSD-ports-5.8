# $OpenBSD: cmake.port.mk,v 1.46 2015/07/01 08:08:18 dcoppa Exp $

BUILD_DEPENDS+=	devel/cmake>=3.2.3p1

.for _n _v in ${SHARED_LIBS}
CONFIGURE_ENV+=LIB${_n}_VERSION=${_v}
MAKE_ENV+=LIB${_n}_VERSION=${_v}
.endfor

USE_NINJA ?= Yes

# XXX: CMake's built-in ELF parser is broken on arm
# XXX: Ninja is broken on m88k
.if ${MACHINE_ARCH} == "arm" || ${MACHINE_ARCH} == "m88k"
USE_NINJA = No
.endif

.if ${USE_NINJA:L} == "yes"
BUILD_DEPENDS += devel/ninja>=1.5.1
_MODCMAKE_GEN = Ninja
NINJA ?= ninja
NINJA_FLAGS ?= -v -j ${MAKE_JOBS}
MODCMAKE_BUILD_TARGET = cd ${WRKBUILD} && exec ${SETENV} ${MAKE_ENV} \
	${NINJA} ${NINJA_FLAGS} ${ALL_TARGET}
MODCMAKE_INSTALL_TARGET = cd ${WRKBUILD} && exec ${SETENV} ${MAKE_ENV} \
	${FAKE_SETUP} ${NINJA} ${NINJA_FLAGS} ${FAKE_TARGET}
MODCMAKE_TEST_TARGET = cd ${WRKBUILD} && exec ${SETENV} ${ALL_TEST_ENV} \
	${NINJA} ${NINJA_FLAGS} ${TEST_FLAGS} ${TEST_TARGET}

.if !target(do-build)
do-build:
	@${MODCMAKE_BUILD_TARGET}
.endif

.if !target(do-install)
do-install:
	@${MODCMAKE_INSTALL_TARGET}
.endif

.if !target(do-test)
do-test:
	@${MODCMAKE_TEST_TARGET}
.endif

.else
_MODCMAKE_GEN = "Unix Makefiles"
# XXX cmake include parser is bogus
DPB_PROPERTIES += nojunk
.endif

CONFIGURE_ENV +=	MODJAVA_VER=${MODJAVA_VER} \
			MODLUA_VERSION=${MODLUA_VERSION} \
			MODLUA_BIN=${MODLUA_BIN} \
			MODLUA_INCL_DIR=${MODLUA_INCL_DIR} \
			MODPY_VERSION=${MODPY_VERSION} \
			MODPY_BIN=${MODPY_BIN} \
			MODPY_INCDIR=${MODPY_INCDIR} \
			MODPY_LIBDIR=${MODPY_LIBDIR} \
			MODRUBY_REV=${MODRUBY_REV} \
			MODTCL_VERSION=${MODTCL_VERSION} \
			MODTK_VERSION=${MODTK_VERSION} \
			MODTCL_INCDIR=${MODTCL_INCDIR} \
			MODTK_INCDIR=${MODTK_INCDIR} \
			MODTCL_LIBDIR=${MODTCL_LIBDIR} \
			MODTK_LIBDIR=${MODTK_LIBDIR} \
			MODTCL_LIB=${MODTCL_LIB} \
			MODTK_LIB=${MODTK_LIB}

.if empty(CONFIGURE_STYLE)
CONFIGURE_STYLE=	cmake
.endif
MODCMAKE_configure=	cd ${WRKBUILD} && ${_SYSTRACE_CMD} ${SETENV} \
	CC="${CC}" CFLAGS="${CFLAGS}" \
	CXX="${CXX}" CXXFLAGS="${CXXFLAGS}" \
	${CONFIGURE_ENV} ${LOCALBASE}/bin/cmake \
		-DCMAKE_SKIP_INSTALL_ALL_DEPENDENCY:Bool=True \
		-G ${_MODCMAKE_GEN} ${CONFIGURE_ARGS} ${WRKSRC}

.if defined(DEBUG)
CONFIGURE_ARGS += -DCMAKE_BUILD_TYPE:String=Debug
MODCMAKE_BUILD_SUFFIX =	-debug.cmake
.else
CONFIGURE_ARGS += -DCMAKE_BUILD_TYPE:String=Release
MODCMAKE_BUILD_SUFFIX =	-release.cmake
.endif
SUBST_VARS +=	MODCMAKE_BUILD_SUFFIX

SEPARATE_BUILD ?=	Yes

TEST_TARGET ?=	test

MODCMAKE_WANTCOLOR ?= No
MODCMAKE_VERBOSE ?= Yes

.if ${MODCMAKE_WANTCOLOR:L} == "yes" && defined(TERM)
MAKE_ENV += TERM=${TERM}
.endif

.if ${MODCMAKE_VERBOSE:L} == "yes"
MAKE_ENV += VERBOSE=1
.endif

