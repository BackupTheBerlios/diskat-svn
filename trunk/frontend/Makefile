HTDOCS_ROOT=C:/usr/apache/Apache2/htdocs
WEBAPP=diskat

FILES = categories.php \
categories.php_html \
config.inc \
empty.html \
file_actions.php \
file_category.php \
file_details.php_html \
file_notes.php \
file_notes.php_html \
dir_browse.php \
disk_actions.php \
disk_browse.php \
disk_category.php \
disk_details.php_html \
include/common.php \
include/db.php \
include/Category.php \
include/Disk.php \
include/File.php \
include/html.php \
include/html_db.php \
include/Messages.php \
include/misc.php \
index.html \
menu.php \
menu.php_html \
run_fileman.php \
search.php \
search.php_html \
search_adv.php \
search_adv.php_html \
search_adv_disk.php \
search_adv_disk.php_html \
search_disks.php_html \
t.php \
style.css \
images/* \
js/* \

install:
	rm -rf $(HTDOCS_ROOT)/$(WEBAPP)
	mkdir -p $(HTDOCS_ROOT)/$(WEBAPP)
	cp -r --parents $(FILES) $(HTDOCS_ROOT)/$(WEBAPP)
	chmod -R +r $(HTDOCS_ROOT)/$(WEBAPP)

