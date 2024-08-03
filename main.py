try:
    import sql
    import os
    import logging
except Exception:
    print("incorrect value for connection or ipaddress subnet in .env file")
    exit(0)

def menu():  # for show menu and select item in menu
    logging.debug("run menu")
    while True:

        print("_"*80)
        print(" "*20+"Please Select Number(1-4) AND Enter (0) For Exit")
        print("1.Add User")
        print("2.Show ALLUser")
        print("3.Search User")
        print("4.Update User (name)")
        print("5.Remove User By Search")
        print("6.Remove ALLUser")
        print("0.Exit")
        print("_"*80)
        logging.info("waiting for select item in menu")

        inp = input("Waiting For Select Number From Menu >>> : ").strip()

        if inp.isnumeric() and len(inp) == 1:  # for check the value entered user
            inp = int(inp)

            if inp == 0:
                os.system("clear")
                logging.info("exit")
                exit(0)

            elif inp == 1:
                logging.info("add user selected")
                add()

            elif inp == 2:
                os.system("clear")
                show()

            elif inp == 3:
                logging.info("search user selected")

                search()

            elif inp == 4:
                logging.info("update user selected")

                updateuse()

            elif inp == 5:
                logging.info("delete user selected")

                remove()

            elif inp == 6:
                logging.debug("delete all user selected")

                logging.debug("check to make sure all are removed")
                inp = input(
                    "Delete Allusers , Are You Sure All Are Aemoved ?(y/n) :").strip()

                if inp.lower() == 'y':
                    os.system("clear")
                    logging.info("delet all user done")

                    removeall()
                else:
                    os.system("clear")
                    logging.info("opt out for delete all user")

                    menu()

            else:
                os.system("clear")
                logging.info("invalid input")

                menu()
        else:
            logging.info("invalid input")


def add():  # for enter user
    logging.debug(
        "waiting for the name to be added to the database and ip assigned")

    user = input(
        "Name Of User For Add AND ((For Back To Menu Enter 0))  >>> ").strip()

    if user.isnumeric() and len(user) == 1:

        if int(user) == 0:
            os.system("clear")
            logging.info("selected show menu")

            menu()

        else:
            logging.info("invalid input")

            add()
        logging.info("check user for exist or not exist")

    elif user.isidentifier():

        if sql.searchf(use=user) != 1:  # if user not exist add to database
            logging.info("user not exist")
            logging.info("user added")
            sql.insert(use=user)
            print(f"{user} ADDED")

        add()
    else:
        logging.info("invalid input")

        add()


def show():  # for show all user in database

    print('_'*20 + 'Show ALLUser' + '_'*20)
    sql.show()


def search():  # for search user in database
    logging.debug("waiting for the name to search")
    inp = input(
        "Enter Name For Search AND ((For Back To Menu Enter 0)) >>> : ").strip()

    if inp == '0':
        os.system("clear")
        logging.info("selected show menu")

        menu()

    if inp.isidentifier():
        logging.debug("check the user exist or not exist for show ")

        if sql.search(inp) == 1:
            logging.info("user exist")
            search()

        else:
            logging.info("user not exist")
            print(f"NOT EXIST {inp} IN DATABASE")
            search()

    else:
        logging.info("invalid input")

        search()


def updateuse():  # for search user in database
    global inpp
    logging.debug("waiting for the name to search")
    inpp = input(
        "Enter Name For Search AND ((For Back To Menu Enter 0)) >>> : ").strip()

    if inpp == '0':
        os.system("clear")
        logging.info("selected show menu")

        menu()

    if inpp.isidentifier():
        logging.debug("check the user exist or not exist for update ")

        if sql.search(inpp) == 1:

            logging.info("user exist")
            updateuse2()
        else:
            logging.info("user not exist")
            print(f"NOT EXIST {inpp} IN DATABASE")
            updateuse()

    else:
        logging.info("invalid input")

        updateuse()


def updateuse2():
    updinp = input(
        f"Enter Name For Update {inpp} AND ((For Back To Menu Enter 0)) >>> : ").strip()
    if sql.search(updinp) != 1:

        sql.update(inpp, updinp)
        logging.debug("update user done ")
        print(f'user {inpp} update to {updinp}')
        updateuse()
    else:
        print('_'*20+"User Exist :)"+'_'*20)
        updateuse2()


def remove():  # for delete user in database
    logging.debug("waiting for the name to delete")

    inp = input(
        "Enter Name For Remove AND ((For Back To Menu Enter 0)) >>> : ").strip()

    if inp == '0':
        os.system("clear")
        logging.info("selected show menu")

        menu()

    if inp.isidentifier():
        logging.debug("check the user exist or not exist for delete")

        if sql.delet(inp) == 1:
            logging.info("user deleted")

            remove()

        else:
            logging.info("user not exist for delete")

            print(f"NOT EXIST {inp} IN DATABASE")
            remove()

    else:
        logging.info("invalid input")

        remove()


def removeall():  # for delete all user in databse
    sql.deletall()


if __name__ == '__main__':

    if sql.errorsql == 1 or sql.errordhcp == 1:
        print("please set the local variables in the .env file correctly")
    else:
        os.system('clear')
        menu()
