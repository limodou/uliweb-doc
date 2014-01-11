cd zh_CN
parm make -d ..\..\..\uliweb-doc-static\zh_CN
cd ..\en
parm make -d ..\..\..\uliweb-doc-static\en
cd ..
copy /Y index.html ..\..\uliweb-doc-static
