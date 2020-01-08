import random

def draw_shield(game_box, row, col):
	game_box.addstr(row, col, "   |\\                     /)")
	game_box.addstr(row + 1 , col, " /\\_\\\\__               (_//")
	game_box.addstr(row + 2, col, "|   `>\\-`     _._       //`)")
	game_box.addstr(row + 3, col, " \\ /` \\\\  _.-`:::`-._  //")
	game_box.addstr(row + 4, col, "  `    \\|`    :::    `|/")
	game_box.addstr(row + 5, col, "        |     :::     |")
	game_box.addstr(row + 6, col, "        |.....:::.....|")
	game_box.addstr(row + 7, col, "        |:::::::::::::|")
	game_box.addstr(row + 8, col, "        |     :::     |")
	game_box.addstr(row + 9, col, "        \\     :::     /")
	game_box.addstr(row + 10, col, "         \\    :::    /")
	game_box.addstr(row + 11, col, "          `-. ::: .-'")
	game_box.addstr(row + 12, col, "           //`:::`\\\\")
	game_box.addstr(row + 13, col, "          //   '   \\\\")
	game_box.addstr(row + 14, col, "         |/         \\\\")



def draw_fire(game_box, row, col):
	game_box.addstr(row, col, "#       ")
	game_box.addstr(row + 1 , col, "     #  ")
	game_box.addstr(row + 2, col, "   #  # ")
	game_box.addstr(row + 3, col, "   ##   ")
	game_box.addstr(row + 4, col, "   ##   ")
	game_box.addstr(row + 5, col, "#  ###  ")
	game_box.addstr(row + 6, col, "   #!## ")
	game_box.addstr(row + 7, col, "   #!!# ")
	game_box.addstr(row + 8, col, "  ##!!##")
	game_box.addstr(row + 9, col, " ##!!!##")
	game_box.addstr(row + 10, col, "###!. !##")
	game_box.addstr(row + 11, col, "##!....!#")
	game_box.addstr(row + 12, col, "#!.. ..!#")
	game_box.addstr(row + 13, col, " #!...!# ")
	game_box.addstr(row + 14, col, "  #!!!#  ")


def draw_dagger(game_box, row, col):
	game_box.addstr(row, col, "    /|")
	game_box.addstr(row + 1 , col, "   |\\|")
	game_box.addstr(row + 2, col, "   |||")
	game_box.addstr(row + 3, col, "   |||")
	game_box.addstr(row + 4, col, "   |||")
	game_box.addstr(row + 5, col, "   |||")
	game_box.addstr(row + 6, col, "   |||")
	game_box.addstr(row + 7, col, "   |||")
	game_box.addstr(row + 8, col, "   |||")
	game_box.addstr(row + 9, col, "   |||")
	game_box.addstr(row + 10, col, "   |||")
	game_box.addstr(row + 11, col, "~-[{o}]-~")
	game_box.addstr(row + 12, col, "   |/|")
	game_box.addstr(row + 13, col, "   |/|")
	game_box.addstr(row + 14, col, "   `0'")


def draw_Rat():
	return_list = []

	return_list.append("(q\_/p)")
	return_list.append(" /. .\.-\"\"\"\"\"-.     ___,")
	return_list.append("=\_t_/=     /  `\  (")
	return_list.append("  )\ ))__ __\   |___)")
	return_list.append(" (/-(/` `nn---'")

	return return_list

def draw_RatKing():
	return_list = []

	return_list.append("  (\_/)")
	return_list.append("  (d b)")
	return_list.append("  /\./\\")
	return_list.append(" ( )\"( )")
	return_list.append(" /\| |/\    \\")
	return_list.append("(  \" \"  )   /")
	return_list.append(" \ /~\ / \  \\")
	return_list.append("  \| |/   \_/")
	return_list.append("   \" \"     ")

	return return_list

def draw_SkeletonGrunt():
	return_list = []

	return_list.append("             .-.")
	return_list.append("            (o.o)")
	return_list.append("             |=|")
	return_list.append("            __|__")
	return_list.append("          //.=|=.\\\\")
	return_list.append("         // .=|=. \\\\")
	return_list.append("         \\\\ .=|=. //")
	return_list.append("          \\\\(_=_)//")
	return_list.append("           (:| |:)")
	return_list.append("            || ||")
	return_list.append("            () ()")
	return_list.append("            || ||")
	return_list.append("           ==' '==")


	return return_list


# ITEMS
def draw_not_implemented():
	return_list = []

	return_list.append("N")
	return_list.append("/")
	return_list.append("A")

	return return_list

def draw_Longsword():
	return_list = []

	return_list.append("    /")
	return_list.append("O===[====================-")
	return_list.append("    \\")

	return return_list

def draw_RatFangNecklace():
	return_list = []

	return_list.append(" o--o--=:=--o--o")
	return_list.append("/               \\")
	return_list.append("o               o")
	return_list.append(" \             /")
	return_list.append("  o           o")
	return_list.append("   \         /")
	return_list.append("    o       o")
	return_list.append("     \     /")
	return_list.append("      o   o")
	return_list.append("       \_/")
	return_list.append("      /  \\")
	return_list.append("      \  /")
	return_list.append("       \/")

	return return_list


def draw_Rapier():
	return_list = []
	return_list.append("       |")
	return_list.append("       /~\\")
	return_list.append("Oxxxxx|  (|=========================-")
	return_list.append(" \____/\_/")
	return_list.append("       |")

	return return_list


def draw_ChainHelmet():
	return_list = []

	return_list.append("           §§§|§§§")
	return_list.append("      §§§§§§§§|§§§§§§§§")
	return_list.append("    §§§§§§§§§§|§§§§§§§§§§")
	return_list.append("   |||||||||||||||||||||||")
	return_list.append("   §§§§§   §§§|§§§   §§§§§")
	return_list.append("   §§§§§   §§§|§§§   §§§§§")
	return_list.append("   §§§§§§§§§§§|§§§§§§§§§§§")
	return_list.append("   §§§§§§           §§§§§§")
	return_list.append("   §§§§§             §§§§§")
	return_list.append("   §§§§               §§§§")
	return_list.append("   §§§                 §§§")

	return return_list


def draw_ChainMail():
	return_list = []

	return_list.append("        §§§§§§§§§§§§§§")
	return_list.append("  §§§§§§§§§§§§§§§§§§§§§§§§§§")
	return_list.append(" §§§§§§§§§§§§§§§§§§§§§§§§§§§§")
	return_list.append("§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§")
	return_list.append("§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§")
	return_list.append("§§§§  §§§§§§§§§§§§§§§§§§  §§§§")
	return_list.append("§§§   §§§§§§§§§§§§§§§§§§   §§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return_list.append("      §§§§§§§§§§§§§§§§§§")
	return return_list


def draw_LeatherBoots():
	return_list = []


	return_list.append(" ###########")
	return_list.append(" :::::::::::")
	return_list.append(" ###########")
	return_list.append(" ###########")
	return_list.append(" :::::::::::")
	return_list.append(" ###########")
	return_list.append(" ###########")
	return_list.append(" ###########:")
	return_list.append(' """:########::__')
	return_list.append(" ###: :##########:_")
	return_list.append(' ####: ""###########')
	return_list.append(" ####################")

	return return_list



def draw_alchemy():
	return_list = []

	return_list.append("   ) ))")
	return_list.append("  ( ((  /)")
	return_list.append(" ,-===-//")
	return_list.append("|`-===-'|")
	return_list.append("|       |")
	return_list.append(" \_____/")

	return return_list

def draw_alchemy_alternate():
	return_list = []



	return_list.append("   ( ((")
	return_list.append("   ) )) /)")
	return_list.append(" ,-===-//")
	return_list.append("|`-===-'|")
	return_list.append("|       |")
	return_list.append(" \_____/")

	return return_list


def draw_alchemy_fire():
	return_list = []

	return_list.append(" ((%(%))")
	return_list.append(".-'...`-.")
	return_list.append("`-'..'`-'")

	return return_list

def draw_alchemy_fire_alternate():
	return_list = []

	return_list.append(" ))&)&((")
	return_list.append(".-'...`-.")
	return_list.append("`-'..'`-'")

	return return_list


def draw_juicer():
	return_list = []

	return_list.append("    |-------\\")
	return_list.append("  \\===/     |")
	return_list.append("   |        |")
	return_list.append("     |      |")
	return_list.append(" .=====.    |")
	return_list.append(" |     |    |")
	return_list.append(" \_____/  __|__")


	return return_list

def draw_juicer_alternate():
	return_list = []

	return_list.append("    |-------\\")
	return_list.append("  \\===/     |")
	return_list.append("     |      |")
	return_list.append("   |        |")
	return_list.append(" .=====.    |")
	return_list.append(" |     |    |")
	return_list.append(" \_____/  __|__")


	return return_list


def draw_portrait_dwarf():
	return_list = []

	return_list.append("###########")
	return_list.append("### #### ##")
	return_list.append("###########")
	return_list.append("###########")
	return_list.append("# ####### #")
	return_list.append("##   ##  ##")
	return_list.append("#####  ####")
	return_list.append("###########")

	return return_list


def draw_key():
	return_list = []

	return_list.append("  8 8          ,o. ")
	return_list.append(" d8o8azzzzzzzzd   b")
	return_list.append("               `o'")

	return return_list




def draw_necro_book():
	return_list_1 = []
	return_list_2 = []
	return_list_3 = []
	return_list_4 = []

	return_list_1.append(" .▄▄ ·  ▄▄▄· ▌ ▐·▄▄▄ .    • ▌ ▄ ·. ▄▄▄ .")
	return_list_1.append("▐█ ▀. ▐█ ▀█▪█·█▌▀▄.▀·    ·██ ▐███▪▀▄.▀·")
	return_list_1.append("▄▀▀▀█▄▄█▀▀█▐█▐█•▐▀▀▪▄    ▐█ ▌▐▌▐█·▐▀▀▪▄")
	return_list_1.append("▐█▄▪▐█▐█ ▪▐▌███ ▐█▄▄▌    ██ ██▌▐█▌▐█▄▄▌")
	return_list_1.append(" ▀▀▀▀  ▀  ▀. ▀   ▀▀▀     ▀▀  █▪▀▀▀ ▀▀▀ ")

	return_list_2.append("  ▄ .▄▄▄▄ .▄▄▌   ▄▄▄·    • ▌ ▄ ·. ▄▄▄ .")
	return_list_2.append("██▪▐█▀▄.▀·██•  ▐█ ▄█    ·██ ▐███▪▀▄.▀·")
	return_list_2.append("██▀▐█▐▀▀▪▄██▪   ██▀·    ▐█ ▌▐▌▐█·▐▀▀▪▄")
	return_list_2.append("██▌▐▀▐█▄▄▌▐█▌▐▌▐█▪·•    ██ ██▌▐█▌▐█▄▄▌")
	return_list_2.append("▀▀▀ · ▀▀▀ .▀▀▀ .▀       ▀▀  █▪▀▀▀ ▀▀▀ ")

	return_list_3.append("▪      ·▄▄▄▄            ▐ ▄      ▄▄▄▄▄    ·▄▄▄▄  ▄▄▄ ..▄▄ · ▄▄▄ .▄▄▄   ▌ ▐·▄▄▄ .    ▄▄▄▄▄ ▄ .▄▪  .▄▄ · ")
	return_list_3.append("██     ██▪ ██▪         •█▌▐█▪    •██      ██▪ ██ ▀▄.▀·▐█ ▀. ▀▄.▀·▀▄ █·▪█·█▌▀▄.▀·    •██  ██▪▐███ ▐█ ▀. ")
	return_list_3.append("▐█·    ▐█· ▐█▌▄█▀▄     ▐█▐▐▌ ▄█▀▄ ▐█.▪    ▐█· ▐█▌▐▀▀▪▄▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐█▐█•▐▀▀▪▄     ▐█.▪██▀▐█▐█·▄▀▀▀█▄")
	return_list_3.append("▐█▌    ██. ██▐█▌.▐▌    ██▐█▌▐█▌.▐▌▐█▌·    ██. ██ ▐█▄▄▌▐█▄▪▐█▐█▄▄▌▐█•█▌ ███ ▐█▄▄▌     ▐█▌·██▌▐▀▐█▌▐█▄▪▐█")
	return_list_3.append("▀▀▀    ▀▀▀▀▀• ▀█▄▀▪    ▀▀ █▪ ▀█▄▀▪▀▀▀     ▀▀▀▀▀•  ▀▀▀  ▀▀▀▀  ▀▀▀ .▀  ▀. ▀   ▀▀▀      ▀▀▀ ▀▀▀ ·▀▀▀ ▀▀▀▀ ")

	return random.choice([return_list_1, return_list_2, return_list_3])

if __name__ == "__main__":

	for item in draw_necro_book():
		print(item)