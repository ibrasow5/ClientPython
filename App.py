import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Fonction pour vérifier l'authentification de l'utilisateur
def authenticate_user(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='mglsi_news',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM utilisateurs WHERE username = '{username}' AND mot_de_passe = '{password}'")
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

# Fonction pour afficher la fenêtre principale de gestion des utilisateurs
def manage_users_window():
    def fetch_users():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='mglsi_news',
                user='root',
                password=''
            )
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT id, username, role FROM utilisateurs")
                users = cursor.fetchall()
                user_list.delete(*user_list.get_children())  # Effacer les entrées précédentes
                for user in users:
                    user_list.insert("", "end", values=(user['id'], user['username'], user['role']))
                cursor.close()
                connection.close()
        except Error as e:
            print(f"Error while fetching users: {e}")

    def add_user():
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()

            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='mglsi_news',
                    user='root',
                    password=''
                )
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO utilisateurs (username, mot_de_passe, role) VALUES (%s, %s, %s)",
                                   (username, password, role))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    fetch_users()  # Mettre à jour la liste des utilisateurs après ajout
                    add_user_window.destroy()
            except Error as e:
                print(f"Error while adding user: {e}")

        add_user_window = tk.Toplevel()
        add_user_window.title("Ajouter un utilisateur")

        username_label = tk.Label(add_user_window, text="Nom d'utilisateur :")
        username_label.grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(add_user_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = tk.Label(add_user_window, text="Mot de passe :")
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(add_user_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        role_label = tk.Label(add_user_window, text="Rôle :")
        role_label.grid(row=2, column=0, padx=10, pady=5)
        role_var = tk.StringVar(add_user_window)
        role_var.set("visiteur")  # Valeur par défaut
        role_dropdown = tk.OptionMenu(add_user_window, role_var, "visiteur", "éditeur", "administrateur")
        role_dropdown.grid(row=2, column=1, padx=10, pady=5)

        save_button = tk.Button(add_user_window, text="Enregistrer", command=save_user)
        save_button.grid(row=3, columnspan=2, pady=10)

    def edit_user():
        def save_changes():
            selected_user_id = user_list.item(user_list.selection())['values'][0]
            new_username = username_entry.get()
            new_password = password_entry.get()
            new_role = role_var.get()

            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    database='mglsi_news',
                    user='root',
                    password=''
                )
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute("UPDATE utilisateurs SET username = %s, mot_de_passe = %s, role = %s WHERE id = %s",
                                   (new_username, new_password, new_role, selected_user_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    fetch_users()  # Mettre à jour la liste des utilisateurs après modification
                    edit_user_window.destroy()
            except Error as e:
                print(f"Error while updating user: {e}")

        selected_item = user_list.focus()
        if selected_item:
            edit_user_window = tk.Toplevel()
            edit_user_window.title("Modifier un utilisateur")

            username_label = tk.Label(edit_user_window, text="Nouveau nom d'utilisateur :")
            username_label.grid(row=0, column=0, padx=10, pady=5)
            username_entry = tk.Entry(edit_user_window)
            username_entry.grid(row=0, column=1, padx=10, pady=5)

            password_label = tk.Label(edit_user_window, text="Nouveau mot de passe :")
            password_label.grid(row=1, column=0, padx=10, pady=5)
            password_entry = tk.Entry(edit_user_window, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=5)

            role_label = tk.Label(edit_user_window, text="Nouveau rôle :")
            role_label.grid(row=2, column=0, padx=10, pady=5)
            role_var = tk.StringVar(edit_user_window)
            role_var.set(user_list.item(selected_item)['values'][2])  # Récupérer le rôle actuel
            role_dropdown = tk.OptionMenu(edit_user_window, role_var, "visiteur", "éditeur", "administrateur")
            role_dropdown.grid(row=2, column=1, padx=10, pady=5)

            save_button = tk.Button(edit_user_window, text="Enregistrer", command=save_changes)
            save_button.grid(row=3, columnspan=2, pady=10)
        else:
            messagebox.showerror("Erreur", "Aucun utilisateur sélectionné.")

    def delete_user():
        selected_item = user_list.focus()
        if selected_item:
            confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cet utilisateur ?")
            if confirmation:
                user_id = user_list.item(selected_item)['values'][0]
                try:
                    connection = mysql.connector.connect(
                        host='localhost',
                        database='mglsi_news',
                        user='root',
                        password=''
                    )
                    if connection.is_connected():
                        cursor = connection.cursor()
                        cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (user_id,))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        fetch_users()  # Mettre à jour la liste des utilisateurs après suppression
                except Error as e:
                    print(f"Error while deleting user: {e}")
        else:
            messagebox.showerror("Erreur", "Aucun utilisateur sélectionné.")

    # Création de la fenêtre principale de gestion des utilisateurs
    manage_users_window = tk.Toplevel()
    manage_users_window.title("Gestion des Utilisateurs")

    # Boutons CRUD
    btn_frame = tk.Frame(manage_users_window)
    btn_frame.pack(pady=20)

    add_btn = tk.Button(btn_frame, text="Ajouter un utilisateur", command=add_user)
    add_btn.grid(row=0, column=0, padx=10)

    edit_btn = tk.Button(btn_frame, text="Modifier un utilisateur", command=edit_user)
    edit_btn.grid(row=0, column=1, padx=10)

    delete_btn = tk.Button(btn_frame, text="Supprimer un utilisateur", command=delete_user)
    delete_btn.grid(row=0, column=2, padx=10)

    # Tableau des utilisateurs
    user_list_frame = tk.Frame(manage_users_window)
    user_list_frame.pack(padx=20, pady=10)

    columns = ("ID", "Nom d'utilisateur", "Rôle")
    user_list = ttk.Treeview(user_list_frame, columns=columns, show='headings')
    user_list.heading("ID", text="ID")
    user_list.heading("Nom d'utilisateur", text="Nom d'utilisateur")
    user_list.heading("Rôle", text="Rôle")
    user_list.pack()

    fetch_users()  # Charger les utilisateurs au démarrage de la fenêtre

    # Boucler la fenêtre de gestion des utilisateurs
    manage_users_window.mainloop()

# Fonction pour afficher la fenêtre principale de connexion
def main_window():
    def login():
        username = username_entry.get()
        password = password_entry.get()

        # Authentification de l'utilisateur
        user = authenticate_user(username, password)

        if user is not None and user['role'] == 'administrateur':
            root.destroy()  # Fermer la fenêtre principale de connexion
            manage_users_window()  # Ouvrir la fenêtre de gestion des utilisateurs
        else:
            messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou mot de passe incorrect.")


    # Création de la fenêtre principalea
    root = tk.Tk()
    root.title("Gestion des Utilisateurs")
    root.geometry("400x200")

    # Éléments de la fenêtre principale
    frame = tk.Frame(root)
    frame.pack(pady=20)

    username_label = tk.Label(frame, text="Nom d'utilisateur :")
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = tk.Label(frame, text="Mot de passe :")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    login_button = tk.Button(frame, text="Connexion", command=login)
    login_button.grid(row=2, columnspan=2, pady=10)

    root.mainloop()

# Appel de la fenêtre principale au lancement de l'application
if __name__ == "__main__":
    main_window()
