%global pkg_name saxon
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Java XPath, XSLT 2.0 and XQuery implementation
Name:           %{?scl_prefix}%{pkg_name}
Version:        9.3.0.4
Release:        11.12%{?dist}
# net.sf.saxon.om.XMLChar is from ASL-licensed Xerces
# net/sf/saxon/option/jdom/ is MPLv1.1
# net/sf/saxon/serialize/codenorm/ is UCD
# net/sf/saxon/expr/sort/GenericSorter.java is MIT
# net/sf/saxon/expr/Tokenizer.java and few other bits are BSD
License:        MPLv1.0 and MPLv1.1 and ASL 1.1 and UCD and MIT
URL:            http://saxon.sourceforge.net/
Source0:        https://downloads.sourceforge.net/project/saxon/Saxon-HE/9.3/saxon9-3-0-4source.zip
Source1:        %{pkg_name}.saxon.script
Source2:        %{pkg_name}.saxonq.script
Source3:        %{pkg_name}.build.script
Source4:        %{pkg_name}.1
Source5:        %{pkg_name}q.1
Source6:        https://downloads.sourceforge.net/project/saxon/Saxon-HE/9.3/saxon-resources9-3.zip
Source7:        http://irrational.googlecode.com/svn/trunk/maven-repo/net/sf/saxon/saxon-he/9.3.0.4/saxon-he-9.3.0.4.pom
Source8:        http://www.mozilla.org/MPL/1.0/index.txt#/mpl-1.0.txt
Source9:        http://www.mozilla.org/MPL/1.0/index.txt#/mpl-1.1.txt
BuildRequires:  unzip
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}bea-stax-api
BuildRequires:  %{?scl_prefix_java_common}xml-commons-apis
BuildRequires:  %{?scl_prefix_java_common}jdom >= 0:1.0-0.b7
BuildRequires:  %{?scl_prefix_java_common}dom4j
Requires:       %{?scl_prefix_java_common}bea-stax-api
Requires:       %{?scl_prefix_java_common}bea-stax

# Older versions were split into multile packages

BuildArch:      noarch

%description
Saxon HE is Saxonica's non-schema-aware implementation of the XPath 2.0,
XSLT 2.0, and XQuery 1.0 specifications aligned with the W3C Candidate
Recommendation published on 3 November 2005. It is a complete and
conformant implementation, providing all the mandatory features of
those specifications and nearly all the optional features.


%package        manual
Summary:        Manual for %{pkg_name}
Requires:       %{?scl_prefix}runtime

%description    manual
Manual for %{pkg_name}.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%package        demo
Summary:        Demos for %{pkg_name}
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{pkg_name}.

%package        scripts
Summary:        Utility scripts for %{pkg_name}
Requires:       %{?scl_prefix_java_common}jpackage-utils >= 0:1.5
Requires:       %{name} = %{version}-%{release}

%description    scripts
Utility scripts for %{pkg_name}.


%prep
%setup -q -c -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

unzip -q %{SOURCE6}
cp -p %{SOURCE3} ./build.xml

# deadNET
rm -rf net/sf/saxon/dotnet samples/cs

# Depends on XQJ (javax.xml.xquery)
rm -rf net/sf/saxon/xqj

# XOM support is not wanted
rm -rf ./doc/javadoc/net/sf/saxon/option/xom
rm -rf ./net/sf/saxon/option/xom

# This requires a EE edition feature (com.saxonica.xsltextn)
rm -rf net/sf/saxon/option/sql/SQLElementFactory.java

# cleanup unnecessary stuff we'll build ourselves
rm -rf docs/api
find . \( -name "*.jar" -name "*.pyc" \) -delete

cp %{SOURCE8} %{SOURCE9} .
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
mkdir -p build/classes
echo "config=net.sf.saxon.Configuration
platform=net.sf.saxon.java.JavaPlatform" > build/classes/edition.properties

export CLASSPATH=$(build-classpath xml-commons-apis jdom bea-stax-api dom4j)
ant \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Djdom.javadoc=%{_javadocdir}/jdom
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{pkg_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{pkg_name}
install -p -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{pkg_name}q
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/%{pkg_name}.1
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/%{pkg_name}q.1


# a simple POM
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
sed -i -e 's/saxon-he/saxon/' $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}


%files -f .mfiles
%defattr(-,root,root,-)
%doc mpl-1.0.txt mpl-1.1.txt

%files manual
%defattr(-,root,root,-)
%doc doc/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{pkg_name}

%files scripts
%defattr(-,root,root,-)
%{_bindir}/%{pkg_name}
%{_bindir}/%{pkg_name}q
%{_mandir}/man1/%{pkg_name}.1*
%{_mandir}/man1/%{pkg_name}q.1*


%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.12
- Remove prebuilt binary files from samples

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.11
- Add requires on SCL filesystem package

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0.4-11.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 9.3.0.4-11.9
- Fix BR/R

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 9.3.0.4-11.8
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 9.3.0.4-11.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.3
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-11.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 9.3.0.4-11
- Mass rebuild 2013-12-27

* Wed Sep 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-10
- Disable support for XOM

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-9
- Remove workaround for rpm bug #646523

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.3.0.4-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 9.3.0.4-6
- Fix license tag properly to include all pieces and add comments

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Andy Grimm <agrimm@gmail.com> - 9.3.0.4-4
- Fix option syntax in scripts when using xml-commons-resolver (#831631)

* Wed Feb 15 2012 Andy Grimm <agrimm@gmail.com> - 9.3.0.4-3
- Fix FTBFS (#791033)
- Add a simple POM file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 17 2011 Alexander Kurtakov <akurtako@redhat.com> 9.3.0.4-1
- Update to new upstream version.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 9.2.0.3-1
- New package, based on saxon8

* Tue Nov 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:8.7-1
- Tidied up for Fedora

* Tue Mar 14 2006 Deepak Bhole <dbhole@redhat.com> - 0:B.8.7-1jpp
- Changed package name for compatibility
- Upgraded to 8.7
- Added saxonq script for queries
- Updated man pages

* Mon Jan 30 2006 Ralph Apel <r.apel@r-apel.de> - 0:8.6.1-1jpp
- Derive saxonb8 from saxon7

* Mon Sep 05 2005 Ralph Apel <r.apel@r-apel.de> - 0:7.9.1-1jpp
- Derive saxon7 from saxon
- no more aelfred nor fop subpackages

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> - 0:6.5.3-3jpp
- Rebuilt with Ant 1.6.2

* Mon Jul 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.3-2jpp
- Apply two patches for known limitations from
  http://saxon.sourceforge.net/saxon6.5.3/limitations.html
- Make the command line script use xml-commons-resolver if it's available.
- Include man page for command line script.
- Add patch to fix command line option handling and document missing options.
- New style versionless javadoc dir symlinking.
- Crosslink with local J2SE javadocs.
- Add missing jdom-javadoc build dependency.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.3-1jpp
- Update to 6.5.3.
- Crosslink with local xml-commons-apis and fop javadocs.

* Tue Jun  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.2-7jpp
- Non-versioned javadoc symlinking.
- Include Main-Class attribute in saxon.jar.
- Own (ghost) %%{_javadir}/jaxp_transform_impl.jar.
- Remove alternatives in preun instead of postun.

* Thu Apr 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 6.5.2-6jpp
- Rebuild for JPackage 1.5.
- Split shell script to -scripts subpackage.
- Use non-versioned jar in jaxp_transform_impl alternative, and don't remove
  it on upgrade.
- Spec file cleanups.

* Thu Jul 25 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-5jpp
- Fix shell script (again).
- Rebuild with -Dbuild.compiler=modern (saxon-fop won't build with jikes).

* Fri Jul 19 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-4jpp
- First public JPackage release.
- Compile with build.xml by yours truly.
- AElfred no more provides jaxp_parser_impl; it's SAX only, no DOM.
- Fix shell script.

* Mon Jul  1 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-3jpp
- Provides jaxp_parser_impl.
- Requires xml-commons-apis.

* Sun Jun 30 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-2jpp
- Use sed instead of bash 2 extension when symlinking jars.
- Provides jaxp_transform_impl.

* Sat May 11 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-1jpp
- First JPackage release.
- Provides jaxp_parser2 though there's no DOM implementation in this AElfred.
