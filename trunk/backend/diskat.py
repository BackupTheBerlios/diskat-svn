import sys
import stat
import string
import getopt
import sqlite
import Volume
import App
import util

CMD_ADD    = 1
CMD_DELETE = 2
CMD_UPDATE = 3
command = 0
command_arg = None

def usage():
    sys.stdout.write("discat.py - DiskCat disk cataloging system command-line client\n")
    sys.stdout.write("Usage: discat.py <options> <command> <arguments>\n")
    sys.stdout.write("  Commands:\n")
    sys.stdout.write("	-a <disk_path>, --add=<disk_path> - add disk to catalog\n")
    sys.stdout.write("	-d <disk_tag>,  --delete=<disk_tag> - delete disk from catalog\n")
    sys.stdout.write("	-u <disk_tag>,  --update=<disk_tag> - update catalogued disk's contents\n")
    sys.stdout.write("	Add is the default command (you can just specify path)\n")
    sys.stdout.write("  Options:\n")
    sys.stdout.write("	--quiet - don't ask questions if possible\n")
    sys.stdout.write("	--no-archives - do not catalogue archive contents\n")
    sys.stdout.write("	--tag= - set disk tag (else ask)\n")
    sys.stdout.write("	--title= - set disk title (else ask)\n")
    sys.stdout.write("	--path= - override disk's mount path (useful with -u)\n")
    sys.exit(1)

def set_command(cmd, param):
    global command, command_arg
    if command != 0: usage()
    command = cmd
    command_arg = param

def enterTag():
    while 1:
        tag = raw_input("Enter disk tag (ID by which the disk will be identified): ")
        tag = string.strip(tag)
        if len(tag) > 0: 
            if not app.checkDiskTag(tag):
                print "Disk with such tag already exists"
            else:
                return tag

def add_operation(opts):
    v = Volume.Volume(opts.get("--path", command_arg))
    ser_num = v.getSerialNumber()
    label = v.getLabel()
    print "Adding disk: Serial Number %s, Label '%s'" % (ser_num, label)

    disk = app.findDiskBySerialAndLabel(ser_num, label)
    if not opts.has_key("--quiet"):
        if disk:
            answer = raw_input("Disk with such serial and label already exists, continue (y/n)? ")
            if answer != "y":
                return
        else:
            print "Disk not yet catalogued"

    if opts.has_key("--tag"):
        tag = opts["--tag"]
    else:
        tag = enterTag()

    if opts.has_key("--title"):
        title = opts["--title"]
    elif opts.has_key("--quiet"):
        title = ""
    else:
        title = raw_input("Enter disk title: ")
    title = util.oem2ansi(title)

    id = app.addDisk(v, tag, title)
    if opts.has_key("--no-archive"):
        v.setRecurseArchives(0)
    sys.stdout.write("Adding files: ")
    stats = app.catalogDisk(v, id)
    app.commit()
    printStats(stats)

def update_operation(opts):
    disk = app.findDiskByTag(opts.get("--tag", command_arg))
    if not disk:
        add_operation(opts)
    else:
        v = Volume.Volume(opts.get("--path", disk.root))
        app.clearDiskContents(disk.id)
        if opts.has_key("--no-archive"):
            v.setRecurseArchives(0)
        sys.stdout.write("Adding files: ")
        stats = app.catalogDisk(v, disk.id)
        app.commit()
        print "Updated disk", command_arg
        printStats(stats)

def delete_operation(opts):
    disk = app.findDiskByTag(command_arg)
    if not disk:
        print "Disk not found"
    else:
        app.deleteDisk(disk.id)
        app.commit()
        print "Deleted disk", command_arg

def printStats(stats):
    print "Real files       : % 6d (% 6d directories + % 6d files)" \
      % (stats[0] + stats[1], stats[1], stats[0])
    print "Files in archives: % 6d (% 6d directories + % 6d files)" \
      % (stats[2] + stats[3], stats[3], stats[2])
    print "============================================================="
    print "Total            : % 6d" \
      % (stats[0] + stats[1] + stats[2] + stats[3])

optlist, args = getopt.getopt(
  sys.argv[1:], "h?a:d:u:", ["add=", "delete=", "update=", "no-archive", "quiet", "tag=", "title=", "path="]
)
opts = {}
for opt, param in optlist:
    if opt=='-h' or opt=='-?': usage()
    if opt in ["-a", "--add"]: set_command(CMD_ADD, param)
    if opt in ["-d", "--delete"]: set_command(CMD_DELETE, param)
    if opt in ["-u", "--update"]: set_command(CMD_UPDATE, param)
    opts[opt] = param

if command == 0 and len(args) == 1:
   command = CMD_ADD
   command_arg = args[0]

if command == 0: usage()

app = App.App()
if command == CMD_ADD: 
    add_operation(opts)
elif command == CMD_DELETE: 
    delete_operation(opts)
elif command == CMD_UPDATE: 
    update_operation(opts)



