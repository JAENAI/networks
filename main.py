import client as c
import server as s
import threading
import sys
import os 

if __name__=='__main__':

   #Checking arguments
    
    if len(sys.argv)<7 or len(sys.argv)>9:
        print(f"Usage : \n")
        print(f" for server : python3 main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
        print(f" or  python main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
        print(f" for clients : python3 main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")
        print(f" or  python main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")
    
    else:
        if sys.argv[1]=="--server":
            if not(os.path.exists(sys.argv[3])):
                print(f"File doesn't exist")
            elif os.path.getsize(sys.argv[3])>=10000000000:
                print(f"File too heavy!")
            elif len(sys.argv)==9:
                # Creating server 
                print(f"Server is starting")
                new_serv=s.Server(int(sys.argv[2]),sys.argv[3],float(sys.argv[4]),float(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]))
                new_serv.start()
            else:
                print(f"Wrong number of arguments. \n")
                print(f"Try:\n")
                print(f" for server : python3 main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
                print(f" or  python main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
        elif sys.argv[1]=="--clients":
            if not(os.path.exists(sys.argv[3])):
                print(f"File doesn't exist")
            elif os.path.getsize(sys.argv[3])>=10000000000:
                print(f"File too heavy!")
            elif len(sys.argv)==7:
                #Creating clients
                clients=[]
                client_threads=[]
                for i in range(int(sys.argv[2])):
                    print(f"Client {i+1} is starting")
                    client=c.Client(i+1,int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
                    thread=threading.Thread(target=client.start,args=())
                    client_threads.append(thread)

                for thread in client_threads:
                    thread.start()
        
                for thread in client_threads:
                    thread.join()
            else:
                print(f"Wrong number of arguments. \n")
                print(f"Try:\n")
                print(f" for clients : python3 main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")
                print(f" or  python main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")
        else:
            print(f"Usage : \n")
            print(f" for server : python3 main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
            print(f" or  python main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]\n ")
            print(f" for clients : python3 main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")
            print(f" or  python main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]\n ")





    
    
    



