import sys
import json

def init_test():
    # Data to be written
    init_test = {
        "Total_Test_Number": 0,
        "Test_List": [],
    }
# Serializing json
    json_object = json.dumps(init_test, indent=4)
# Writing to init_test.json
    with open("./test/test.json", "w") as outfile:
        outfile.write(json_object)

if __name__=="__main__":
    sys.path.append('test')
    try:
        with open('./test/test.json', 'r') as f:
            test_dict = json.load(f)
            print("loaded test.json")
            # validate test.json
            if not ("Total_Test_Number" in test_dict.keys() and "Test_List" in test_dict.keys()):
                init_test()
                print("test.json is invalid, reinitialized")
    except:
        init_test()
        print("test.json is not found, initialized")
    
    # Ask user to enter test number
    while True:
        flag = input("\nPlease enter 1 to view the tests, 2 to add a new test, 3 to edit the tests, 4 to delete a test, 5 to exit: ")
        if flag == "1":
            print("\nTostal Test Number:  ", test_dict["Total_Test_Number"], "\n")
            if test_dict["Total_Test_Number"] == 0:
                print("There is no test in the list.")
            else:
                for i in range(test_dict["Total_Test_Number"]):
                    print("Test", i+1, ": ", test_dict["Test_List"][i])
        if flag == "2":
            test_name = input("Please enter test name: ")
            test_dict["Test_List"].append(test_name)
            test_dict["Total_Test_Number"] += 1
            with open("./test/test.json", "w") as outfile:
                json.dump(test_dict, outfile)
            print(test_name , "is added.")
            
        if flag == "3":
            test_number = input("Please enter test number: ")
            if int(test_number) > test_dict["Total_Test_Number"]:
                print("Invalid test number.")
            else:
                test_name = input("Please enter test name: ")
                test_dict["Test_List"][int(test_number)-1] = test_name
                with open("./test/test.json", "w") as outfile:
                    json.dump(test_dict, outfile)
                print("Test", test_number, "is changed to", test_name)
            
        if flag == "4":
            test_number = input("Please enter test number: ")
            if int(test_number) > test_dict["Total_Test_Number"]:
                print("Invalid test number.")
            else:
                test_dict["Test_List"].pop(int(test_number)-1)
                test_dict["Total_Test_Number"] -= 1
                with open("./test/test.json", "w") as outfile:
                    json.dump(test_dict, outfile)
                print("Test", test_number, "is deleted.")
        if flag == "5":
            break
        #test_number = input("Please enter test number: ")
    
        
        

