# Networks 



Project done for simulation of multiple clients downloading a file.

The server should first and then the clients.

Usage :
    for server : python3 main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]
                 or  python main.py --server [total_clients] [filename] [probability] [timeout] [buffer_size] [window_size] [number_files]
    for clients : python3 main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]
                 or  python main.py --clients [total_clients] [filename] [buffer_size] [window_size] [number_files]
    