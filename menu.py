import json, webbrowser, sys, mysql.connector
from new_data import text
from new_data import categories
from db_class import Db


class Menu:

    def __init__(self):
        self.data_base = Db()
        self.mycursor = self.data_base.db.cursor()

    def welcome_menu(self):
        print(text[1])
        self.choice = input(text[2])
        print(text[3])
        if self.choice == "i":
            pass
        elif self.choice == "q":
            sys.exit()
        elif self.choice == "a":
            self.display_substitute_list()
        
        else:
            print('Veuillez rentrer un choix valide svp.')  
            self.welcome_menu()

    def set_pages_set_items(self):
        self.first_item = 0
        self.last_item = 20
        self.page = 1

    def choose_categories(self):
        self.x = 1
        for i in categories:
            print("%-5s %s" % (self.x, i))
            self.x += 1            
        self.choice = input("Choisissez une categorie:")

        try:
            self.selected_category = categories[int(self.choice)-1]    
            self.sql = """SELECT nom, marque, productID, nutriscore,
                    store, code_ID  FROM off WHERE category = %s"""
            self.adr = (self.selected_category,)
            self.mycursor.execute(self.sql, self.adr)
            self.myresult = self.mycursor.fetchall()

        except(ValueError, IndexError):
            print('Veuillez rentrer un choix valide svp.') 
            self.choose_categories()

    def display_category(self):
        print("%-10s %-70s %-60s %s" %
                ("Indice", "Marque", "Nom", "#"+self.selected_category))
        print(text[3])
        self.indice = 1
        for x in self.myresult[self.first_item: self.last_item]:
            print("%-10s %-70s %s" % (self.indice, x[1], x[0]))
            self.indice += 1
        print("#" * 60, "PAGE ", self.page, "#" * 76)

    def back_category_or_menu(self):
        if self.nav == "m":
            self.searching_through = False
            self.choosing_categorie = False
        elif self.nav == "c":
            self.searching_through = False            
                
    def product_menu_info(self):
        print(text[3])
        print("%-10s %-70s %-60s %s" % ("Nutriscore", "Marque", "Nom", "Magazin"))
        print(text[3])
        self.sel_items = (self.page - 1) * 20 + int(self.nav) - 1        
        print("%-10s %-70s %-60s %s" % (self.myresult[self.sel_items][3],
                                        self.myresult[self.sel_items][1],
                                        self.myresult[self.sel_items][0], 
                                        self.myresult[self.sel_items][4]))
        print(text[3])

    def display_store_or_off(self):
        if self.nav == "o":
            self.url = "https://fr.openfoodfacts.org/produit/" + str(self.myresult[self.sel_items][5])            
            webbrowser.open_new_tab(self.url)
        elif self.nav == "s":
            self.url = "https://www.google.com/maps/search/?api=1&query=" + str(self.myresult[self.sel_items][4])
            webbrowser.open_new_tab(self.url)

    def menu_action(self):
        try:
            self.nav = input(text[4])
            if self.nav == "n":
                if self.page*20 >= len(self.myresult):
                    pass
                else:
                    self.first_item += 20
                    self.last_item += 20
                    self.page += 1

            elif self.nav == "b":
                if self.first_item == 0:
                    pass
                else:
                    self.first_item -= 20
                    self.last_item -= 20
                    self.page -= 1

            elif self.nav == "m" or self.nav == "c":
                self.back_category_or_menu()         

            elif int(self.nav) > 0 and int(self.nav) <= int(self.indice):
                self.product_menu_info()                    
                self.product_menu()
            
        except(ValueError, IndexError):
            print('Veuillez rentrer un choix valide svp.') 
                   
    def healthy_menu(self):
        self.sql = """SELECT nom, marque, productID, nutriscore, store, code_ID  
            FROM off WHERE category = %s ORDER BY nutriscore ASC"""
        self.adr = (self.selected_category,)
        self.mycursor.execute(self.sql, self.adr)
        self.myresult = self.mycursor.fetchall()    
        print("%-10s %-70s %-60s %s" % ("Indice", "Marque", "Nom", "nutriscore"))
        print(text[3])
        self.indice = 1
        for x in self.myresult[0:20]:
            print("%-10s %-70s %-60s %s" % (self.indice, x[1], x[0], x[3]))
            self.indice += 1
        print(text[5])
        self.nav = input(text[7])
       
        if self.nav == "m" or self.nav == "c":
            self.back_category_or_menu()

        elif int(self.nav) > 0 and int(self.nav) <= int(self.indice):
            self.page = 1
            self.product_menu_info()                       
            self.healthy_choice_product_menu()
        else:
            print('Veuillez rentrer un choix valide svp.')
            self.healthy_menu()   
    
    def healthy_choice_product_menu(self):
        print(text[5])
        self.nav = input(text[8])                
       
        if self.nav == "m" or self.nav == "c":
            self.back_category_or_menu()                    

        elif self.nav == "o" or self.nav == "s":
            self.display_store_or_off()
            self.healthy_choice_product_menu()

        elif self.nav == "l":
            self.healthy_menu()         

        elif self.nav == "z":
            self.mycursor.execute("""CREATE TABLE IF NOT EXISTS substitute 
                                (nom VARCHAR(100), marque VARCHAR(100),
                                category VARCHAR(20), nutriscore VARCHAR(1),
                                store VARCHAR(100), code_id BIGINT)""")
            self.this_productID = (self.myresult[self.sel_items][2])
            self.sql = """INSERT INTO substitute (marque, nom, nutriscore, 
                    store, code_id) SELECT marque, nom, nutriscore, store,
                    code_id FROM off WHERE productID= %s"""
            self.adr = (self.this_productID,)
            self.mycursor.execute(self.sql, self.adr)
            self.data_base.db.commit()
            self.healthy_choice_product_menu()

        else:
            print('Veuillez rentrer un choix valide svp.')
            self.healthy_choice_product_menu()

    def product_menu(self):
        print(text[5])
        self.nav = input(text[9])
       
        if self.nav == "m" or self.nav == "c":
            self.back_category_or_menu()
                          
        elif self.nav == "o" or self.nav == "s":
            self.display_store_or_off()
            self.product_menu()

        elif self.nav == "g":
            self.healthy_menu()

        else:
            print('Veuillez rentrer un choix valide svp.')
            self.product_menu()

    def display_substitute_list(self):
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS substitute 
                            (nom VARCHAR(100), marque VARCHAR(100),
                            category VARCHAR(20), nutriscore VARCHAR(1),
                            store VARCHAR(100), code_id BIGINT)""")
        self.mycursor.execute("SELECT * FROM substitute")
        self.myresult = self.mycursor.fetchall()
        print("%-10s %-70s %-60s %s" %
                ("Indice", "Marque", "Nom", "Nutriscore"))
        print(text[3])
        self.indice = 1
        for x in self.myresult:
            print("%-10s %-70s %-60s %s" % (self.indice, x[1], x[0], x[3]))
            self.indice += 1
        self.healthy_list_menu()

    def healthy_list_menu(self):
        print(text[5])
        self.nav = input(text[6])
       
        if self.nav == "m":
            self.welcome_menu()

        elif self.nav == "e":
            self.mycursor.execute("DROP TABLES substitute")
            self.welcome_menu()

        elif int(self.nav) > 0 and int(self.nav) <= int(self.indice):
            self.healthy_item_menu()

    def healthy_item_menu(self):
        print(text[5])
        self.page = 1
        self.product_menu_info()
        self.healthy_navigation = self.nav[:]
        self.nav = input(text[10])
       
        if self.nav == "m":
            self.welcome_menu()

        elif self.nav == "o" or self.nav == "s":
            self.display_store_or_off()
            self.nav = self.healthy_navigation[:]
            self.healthy_item_menu()

        elif self.nav == "a":
            self.display_substitute_list()               