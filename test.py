
import json
import mysql.connector
from menu import Menu
from db_class import Db
import webbrowser

new_menu= Menu()

while True:
    
    new_menu.welcome_menu()   
    new_menu.choosing_categorie = True

    while new_menu.choosing_categorie == True:

        new_menu.set_pages_set_items()        
        new_menu.choose_categories()    
        new_menu.searching_through = True
         
        while new_menu.searching_through == True:
            new_menu.display_category()            
            new_menu.menu_action()




