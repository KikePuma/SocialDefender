#! /bin/bash
buc="true"
while [ "$buc" = "true" ]; do
	echo "     ___ _       __          _         "
	echo "    / __(_)_ _  / _|___ _ _ (_)___ _ _ "
	echo "    \__ \ | ' \|  _/ _ \ ' \| / -_) '_|"
	echo "    |___/_|_||_|_| \___/_||_|_\___|_|  "
	echo ''
	echo ' Helping Tool 4 Sinfonier © KikePuma 2017'
	echo ''
	echo ' Menu:'
	echo ''
	echo ' [1] Open Sinfonier-Project'
	echo ' [2] Open Drain Sites'
	echo ''
	echo ' [0] Exit'
	echo ''
	read -p " Choose an option: " opt0
	case "$opt0" in
		"0" )
			exit 1;
			;;
		"1" )
			iceweasel http://drawer.sinfonier-project.net &
			iceweasel http://hackaton.sinfonier-project.net &
			buc="false"
			;;
		"2" )
			buc="false"
			intmenu="true"
			while [ "$intmenu" = "true" ]; do
				echo
				echo ' [1] Twitter'
				echo ' [2] Dweet'
				echo ' [3] Mlab'
				echo ' [4] Loggly'
				echo ' [5] Instapush'
				echo
				echo ' [0] Menu'
				echo
				read -p " Choose an option: " opt1
				case "$opt1" in
					"0" )
						intmenu="false"
						buc="true"
						;;
					"1" )
						intmenu="false"
						twmenu="true"
						while [ "$twmenu" = "true" ]; do
							echo
							echo ' [1] Main Page'
							echo ' [2] User Page'
							echo ' [3] Apps Page'
							echo ' [4] APIs Page'
							echo
							echo ' [0] Exit Twitter Menu'
							echo
							read -p " Choose an option: " twopt
							case "$twopt" in
								"1" )
                                                                        iceweasel https://twitter.com &
									exit 1
									;;
								"2" )
                                                                        echo
									read -p "Write the user name without @: " user
									iceweasel https://twitter.com/$user &
                                                                        exit 1;
                                                                        ;;
                                                           	"3" )
                                                                        iceweasel https://apps.twitter.com/ &
									exit 1;
									;;
								"4" )
                                                                        iceweasel https://dev.twitter.com/overview/api &
                                                                        exit 1
                                                                        ;;
								"0" )
									intmenu="true"
									twmenu="false"
									;;
								*)
						                        echo
						                        echo "Please select a correct option"
                        						;;
							esac
						done
						;;
					"2" )
                                                intmenu="false"
                                                dwmenu="true"
                                                while [ "$dwmenu" = "true" ]; do
                                                        echo
                                                        echo ' [1] Main Page'
                                                        echo ' [2] Follow Page'
                                                        echo ' [3] Freeboard'
                                                        echo
                                                        echo ' [0] Exit Dweet Menu'
                                                        echo
                                                        read -p " Choose an option: " dwopt
                                                        case "$dwopt" in
                                                                "1" )
                                                                        iceweasel https://dweet.io &
                                                                        exit 1
                                                                        ;;
                                                                "2" )
                                                                        echo
                                                                        read -p "Write the name of the Dweet: " dweet
                                                                        iceweasel http://dweet.io/follow/$dweet &
                                                                        exit 1;
                                                                        ;;
                                                                "3" )
                                                                        iceweasel https://freeboard.io/ &
                                                                        exit 1;
                                                                        ;;
                                                                "0" )
                                                                        intmenu="true"
                                                                        dwmenu="false"
                                                                        ;;
                                                                *)
									echo
									echo "Please select a correct option"
									;;
							esac
                                                done
						;;
					"3" )
						iceweasel https://mlab.com/login/ &
						exit 1
						;;
					"4" )
						iceweasel https://www.loggly.com/ &
						exit 1
						;;
					"5" )
						iceweasel https://instapush.im/ &
						exit 1
						;;
				esac
			done
			;;
		*)
			echo
			echo "Please select a correct option"
			echo
			;;
		esac
done
