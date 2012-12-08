#!/bin/bash

DIALOG=$(which dialog 2> /dev/null)
XDIALOG=$(which Xdialog 2> /dev/null)
KDIALOG=$(which kdialog 2> /dev/null)
LPC=$(which lpc 2> /dev/null)
NAME=Utils
TITLE='Lexmark $NAME'
BACKTITLE='$TITLE - Conectiva Linux'
ACTION=

mydialog()
{
	local args=$(eval "echo $MYARGS")
	eval "$DIALOG $args $@"
}

msgbox()
{
	local x=$2
	local y=$1
	shift; shift
	mydialog --msgbox "\"$@\"" $y $x
}

menu()
{
	local title="$1"
	shift
	if [ "$DIALOG" = "$KDIALOG" ]; then
		mydialog --menu "\"$title\"" ${1+"$@"}
	else
		mydialog --menu "\"$title\"" 15 60 8 ${1+"$@"}
	fi
}

if [ -n "$DISPLAY" -a -x "$KDIALOG" ]; then
	DIALOG=$KDIALOG
	MYARGS="--title \\\"\"$TITLE\"\\\""
else
	if [ -n "$DISPLAY" -a -x "$XDIALOG" ]; then
		DIALOG=$XDIALOG
		MYARGS="--title \\\"\"$TITLE\"\\\" --backtitle \\\"\"$BACKTITLE\"\\\" --stdout --cr-wrap"
	elif [ ! -t 1 -o ! -t 0 ]; then
		if [ -n "$DISPLAY" ]; then
			xterm=$(which xterm 2> /dev/null)
			if [ -n "$xterm" ]; then
				xterm -c $0 xterm
				exit 1
			fi
		fi
		echo "Can't run under X11 without a terminal!"
		exit 1
	else
		MYARGS="--title \\\"\"$TITLE\"\\\" --backtitle \\\"\"$BACKTITLE\"\\\" --stdout --cr-wrap"
	fi
fi

if [ -z "$DIALOG" ]; then
	echo "Sorry, you must have at least [Xk]dialog installed."
	exit 1
fi

if [ -z "$LPC" ]; then
	msgbox 10 60 "Sorry, couldn't find lpc command."
	exit 1
fi

case "$0" in
	*headalign*)
		ACTION=headalign
		NAME="Head Alignment"
		;;
	*headclean*)
		ACTION=headclean
		NAME="Head Cleaner"
		;;
	*showcartridges*)
		ACTION=showcartridges
		NAME="Show Cartridges"
		;;
	*hidecartridges*)
		ACTION=hidecartridges
		NAME="Hide Cartridges"
		;;
	*)
		msgbox 7 60 "You shouldn't call this directly, sorry."
		exit 1
		;;
esac

ACTION=$(which $ACTION 2> /dev/null)

if [ -z "$ACTION" ]; then
	msgbox 11 60 "Sorry, you must have lxcontrol package installed.\nYou may want to install it by using\napt-get install task-printer-lexmark"
	exit 1
fi

# Check if CUPS is running
lpstat -r >& /dev/null
if [ "$?" -ne "0" ]; then
	msgbox 10 60 "CUPS server is stopped.\nYou must start it and then run this program again."
	exit 1
fi

# Get printers list
if [ "$DIALOG" = "$KDIALOG" ]; then
	printers=$(echo $($LPC status | sort | sed -ne 's/\(.\+\):$/"\1" "\1"/p'))
else
	printers=$(echo $($LPC status | sort | sed -ne 's/\(.\+\):$/"\1" ""/p'))
fi

# Show them to the user, and get the selected one
printer=$(menu 'Please, select the printer:' $printers)
[ "$?" -eq "1" ] && exit 1

# Print it.
$ACTION $printer
if [ "$?" -eq "1" -o -z "$printer" ]; then
	msgbox 11 60 "Something wicked happen while sending the command.\nPlease, take a look at /var/log/cups/error_log\nand report it at http://bugzilla.conectiva.com.br/"
	exit 1
else
	msgbox 9 60 "Command sent successfully!"
fi

exit 0
