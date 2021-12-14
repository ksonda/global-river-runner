@@ -1,63 +0,0 @@
#!/bin/bash
# =================================================================
#
# Authors: Just van den Broecke <justb4@gmail.com>
#
# Copyright (c) 2019 Just van den Broecke
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================
echo "START /build.sh"

set +e
echo "Begining build"
# python3 /scripts/ogr2ogr.py \
#     -f PGDump -lco LAUNDER=NO -lco DROP_TABLE=OFF | gzip > /data/merit_.sql.gz \
#     /data/merit_plus_simplify.gpkg
while [ ! -f /data/merit_plus_simplify.gpkg ]; do echo 1; sleep 1; done
ogr2ogr \
	-f PostgreSQL \
	PG:"host='localhost' \
	    user='${POSTGRES_USER}' \
		password='${POSTGRES_PASSWORD}' \
		dbname='${POSTGRES_DB}'" \
	/data/merit_plus_simplify.gpkg

echo "Done"
# ogr2ogr \
# 	-f PostgreSQL \
# 	PG:"host='localhost' \
# 	    user='${POSTGRES_USER}' \
# 		password='${POSTGRES_PASSWORD}' \
# 		dbname='${POSTGRES_DB}'" \
# 	/data/e_merit_cats.gpkg 

# ogr2ogr \
# 	-f PostgreSQL \
# 	PG:"host='localhost' \
# 	    user='${POSTGRES_USER}' \
# 		password='${POSTGRES_PASSWORD}' \
# 		dbname='${POSTGRES_DB}'" \
# 	/data/w_merit_cats.gpkg 

# rm -rf /data/